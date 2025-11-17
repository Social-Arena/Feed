"""
Session Manager - Manage user content consumption sessions
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta
import random

from ..models.feed import Feed
from ..models.user import User
from .viral_metrics import EngagementEvent
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class SessionConfig:
    """会话配置 - Session configuration"""
    default_time_budget_minutes: float = 30.0
    default_attention_span: float = 1.0
    max_feed_view_time_seconds: float = 30.0
    min_feed_view_time_seconds: float = 2.0

    def to_dict(self) -> Dict:
        return {
            "default_time_budget_minutes": self.default_time_budget_minutes,
            "default_attention_span": self.default_attention_span,
            "max_feed_view_time_seconds": self.max_feed_view_time_seconds,
            "min_feed_view_time_seconds": self.min_feed_view_time_seconds
        }


@dataclass
class SessionParams:
    """会话参数 - Parameters for creating a session"""
    time_budget: float = 30.0  # Minutes
    attention_span: float = 1.0  # Multiplier for attention
    preferences: Dict[str, float] = field(default_factory=dict)
    user_interests: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "time_budget": self.time_budget,
            "attention_span": self.attention_span,
            "preferences": self.preferences,
            "user_interests": self.user_interests
        }


@dataclass
class ContentConsumption:
    """内容消费记录 - Record of content consumption"""
    feed: Feed
    view_time_seconds: float
    engagement: Optional[EngagementEvent]
    viewed_at: datetime
    relevance_score: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "feed_id": self.feed.id,
            "view_time_seconds": self.view_time_seconds,
            "engagement": self.engagement.to_dict() if self.engagement else None,
            "viewed_at": self.viewed_at.isoformat(),
            "relevance_score": self.relevance_score
        }


@dataclass
class ViewDecision:
    """查看决策 - Decision whether to view content"""
    will_view: bool
    reason: str
    confidence: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "will_view": self.will_view,
            "reason": self.reason,
            "confidence": self.confidence
        }


@dataclass
class UserSession:
    """用户会话 - Complete user session"""
    user_id: str
    time_budget: float  # Minutes
    attention_span: float
    preferences: Dict[str, float]
    user_interests: List[str] = field(default_factory=list)

    # Session state
    consumed_content: List[ContentConsumption] = field(default_factory=list)
    engagements: List[EngagementEvent] = field(default_factory=list)
    session_start: datetime = field(default_factory=datetime.utcnow)
    fatigue_level: float = 0.0  # 0-1, increases over session

    @property
    def time_remaining(self) -> float:
        """Calculate remaining session time in minutes"""
        total_view_time = sum(c.view_time_seconds for c in self.consumed_content) / 60
        return max(0, self.time_budget - total_view_time)

    @property
    def content_count(self) -> int:
        """Number of pieces of content consumed"""
        return len(self.consumed_content)

    @property
    def engagement_count(self) -> int:
        """Number of engagements made"""
        return len(self.engagements)

    @property
    def engagement_rate(self) -> float:
        """Session engagement rate"""
        if self.content_count == 0:
            return 0.0
        return self.engagement_count / self.content_count

    def add_consumption(self, consumption: ContentConsumption):
        """Add content consumption to session"""
        self.consumed_content.append(consumption)

        if consumption.engagement:
            self.engagements.append(consumption.engagement)

        # Increase fatigue
        self.fatigue_level = min(1.0, self.fatigue_level + 0.01)

    def update_state(self, feed: Feed, engagement: Optional[EngagementEvent]):
        """Update session state (legacy method for compatibility)"""
        consumption = ContentConsumption(
            feed=feed,
            view_time_seconds=5.0,
            engagement=engagement,
            viewed_at=datetime.utcnow()
        )
        self.add_consumption(consumption)

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "time_budget": self.time_budget,
            "time_remaining": self.time_remaining,
            "content_count": self.content_count,
            "engagement_count": self.engagement_count,
            "engagement_rate": self.engagement_rate,
            "fatigue_level": self.fatigue_level,
            "session_duration_minutes": (datetime.utcnow() - self.session_start).total_seconds() / 60
        }


@dataclass
class SessionResult:
    """会话结果 - Complete session result"""
    session: UserSession
    consumption_log: List[ContentConsumption]
    total_time_spent_minutes: float
    metrics: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "user_id": self.session.user_id,
            "consumption_log": [c.to_dict() for c in self.consumption_log],
            "total_time_spent_minutes": self.total_time_spent_minutes,
            "content_viewed": len(self.consumption_log),
            "engagements": self.session.engagement_count,
            "engagement_rate": self.session.engagement_rate,
            "metrics": self.metrics
        }


class SessionManager:
    """会话管理器 - Manager for user content consumption sessions"""

    def __init__(self, config: Optional[SessionConfig] = None):
        """
        Initialize session manager

        Args:
            config: Session configuration
        """
        self.config = config or SessionConfig()
        self.active_sessions: Dict[str, UserSession] = {}
        self.session_history: List[SessionResult] = []

        logger.info("SessionManager initialized", config=self.config.to_dict())

    @logger.trace_decorator
    def create_user_session(
        self,
        user_id: str,
        session_params: Optional[SessionParams] = None
    ) -> UserSession:
        """
        创建用户会话
        Create new user session

        Args:
            user_id: User identifier
            session_params: Session parameters (uses defaults if None)

        Returns:
            UserSession object
        """
        logger.info(f"Creating session for user {user_id}")

        try:
            params = session_params or SessionParams(
                time_budget=self.config.default_time_budget_minutes,
                attention_span=self.config.default_attention_span
            )

            session = UserSession(
                user_id=user_id,
                time_budget=params.time_budget,
                attention_span=params.attention_span,
                preferences=params.preferences,
                user_interests=params.user_interests
            )

            self.active_sessions[user_id] = session

            logger.info(
                f"Session created for user {user_id}",
                time_budget=params.time_budget,
                attention_span=params.attention_span
            )

            return session

        except Exception as e:
            logger.error(f"Error creating session for user {user_id}", exception=e)
            raise

    @logger.trace_decorator
    def simulate_content_consumption(
        self,
        session: UserSession,
        available_content: List[Feed],
        ranking_function: Optional[Callable[[UserSession, Feed], float]] = None
    ) -> SessionResult:
        """
        模拟内容消费过程
        Simulate content consumption process

        Args:
            session: User session
            available_content: List of feeds available to show
            ranking_function: Optional function to rank/score content

        Returns:
            SessionResult with consumption log
        """
        logger.info(
            f"Simulating consumption for user {session.user_id}",
            available_content=len(available_content),
            time_budget=session.time_budget
        )

        try:
            consumption_log = []
            remaining_time = session.time_budget * 60  # Convert to seconds

            # Rank content if function provided
            if ranking_function:
                scored_content = [
                    (feed, ranking_function(session, feed))
                    for feed in available_content
                ]
                scored_content.sort(key=lambda x: x[1], reverse=True)
                content_to_show = [feed for feed, _ in scored_content]
            else:
                content_to_show = available_content

            for feed in content_to_show:
                if remaining_time <= 0:
                    break

                # User decision: will view this content?
                view_decision = self._make_view_decision(session, feed)

                if view_decision.will_view:
                    # Calculate view time
                    view_time = self._calculate_view_time(feed, session)

                    # Simulate engagement
                    engagement = self._simulate_engagement(feed, session, view_time)

                    # Calculate relevance
                    relevance = self._calculate_relevance(feed, session)

                    # Record consumption
                    consumption = ContentConsumption(
                        feed=feed,
                        view_time_seconds=view_time,
                        engagement=engagement,
                        viewed_at=datetime.utcnow(),
                        relevance_score=relevance
                    )

                    consumption_log.append(consumption)
                    session.add_consumption(consumption)

                    remaining_time -= view_time

            # Calculate metrics
            total_time_spent = (session.time_budget * 60 - remaining_time) / 60

            metrics = {
                "avg_view_time": sum(c.view_time_seconds for c in consumption_log) / len(consumption_log) if consumption_log else 0,
                "avg_relevance": sum(c.relevance_score for c in consumption_log) / len(consumption_log) if consumption_log else 0,
                "completion_rate": (session.time_budget * 60 - remaining_time) / (session.time_budget * 60),
                "fatigue_level": session.fatigue_level
            }

            result = SessionResult(
                session=session,
                consumption_log=consumption_log,
                total_time_spent_minutes=total_time_spent,
                metrics=metrics
            )

            self.session_history.append(result)

            logger.info(
                f"Consumption simulation completed for user {session.user_id}",
                content_viewed=len(consumption_log),
                time_spent_minutes=total_time_spent,
                engagement_rate=session.engagement_rate
            )

            return result

        except Exception as e:
            logger.error(
                f"Error simulating consumption for user {session.user_id}",
                exception=e
            )
            return SessionResult(
                session=session,
                consumption_log=[],
                total_time_spent_minutes=0.0
            )

    def _make_view_decision(self, session: UserSession, feed: Feed) -> ViewDecision:
        """
        做出查看决策
        Make decision whether user will view this content

        Factors:
        - Fatigue level (higher = less likely to view)
        - Content relevance to interests
        - Random factor
        """
        # Base probability decreases with fatigue
        base_prob = 0.8 * (1 - session.fatigue_level * 0.5)

        # Adjust for relevance
        relevance = self._calculate_relevance(feed, session)
        relevance_boost = relevance * 0.3

        # Final probability
        view_prob = base_prob + relevance_boost

        # Random decision
        will_view = random.random() < view_prob

        reason = "viewed" if will_view else "skipped"
        if session.fatigue_level > 0.8:
            reason = "fatigued" if not will_view else "viewed_despite_fatigue"

        return ViewDecision(
            will_view=will_view,
            reason=reason,
            confidence=view_prob
        )

    def _calculate_view_time(self, feed: Feed, session: UserSession) -> float:
        """
        计算查看时间
        Calculate time user spends viewing content

        Factors:
        - Text length
        - Attention span
        - Fatigue level
        """
        # Base time from text length (assume 200 words/min reading speed)
        word_count = len(feed.text.split())
        base_time = (word_count / 200) * 60  # Seconds

        # Adjust for attention span
        adjusted_time = base_time * session.attention_span

        # Reduce for fatigue
        fatigue_factor = 1 - (session.fatigue_level * 0.5)
        final_time = adjusted_time * fatigue_factor

        # Clamp to reasonable bounds
        final_time = max(
            self.config.min_feed_view_time_seconds,
            min(final_time, self.config.max_feed_view_time_seconds)
        )

        return final_time

    def _simulate_engagement(
        self,
        feed: Feed,
        session: UserSession,
        view_time: float
    ) -> Optional[EngagementEvent]:
        """
        模拟互动
        Simulate user engagement with content

        Factors:
        - View time (longer = more likely to engage)
        - Relevance
        - Fatigue
        """
        # Base engagement probability
        base_prob = 0.05

        # Boost for longer view time
        time_boost = min(view_time / self.config.max_feed_view_time_seconds, 1.0) * 0.15

        # Boost for relevance
        relevance = self._calculate_relevance(feed, session)
        relevance_boost = relevance * 0.20

        # Penalty for fatigue
        fatigue_penalty = session.fatigue_level * 0.10

        # Final probability
        engage_prob = base_prob + time_boost + relevance_boost - fatigue_penalty

        # Random decision
        if random.random() > engage_prob:
            return None

        # Determine engagement type
        rand = random.random()
        if rand < 0.70:
            event_type = "like"
        elif rand < 0.85:
            event_type = "retweet"
        elif rand < 0.92:
            event_type = "quote"
        else:
            event_type = "reply"

        return EngagementEvent(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            user_id=session.user_id,
            feed_id=feed.id,
            depth=0
        )

    def _calculate_relevance(self, feed: Feed, session: UserSession) -> float:
        """
        计算相关性
        Calculate content relevance to user

        Factors:
        - Hashtag overlap with interests
        - Keyword matching
        - Default score for unknown content
        """
        if not session.user_interests:
            return 0.5  # Default moderate relevance

        relevance_score = 0.0

        # Check hashtag overlap
        if feed.entities and feed.entities.hashtags:
            feed_hashtags = {tag.tag.lower() for tag in feed.entities.hashtags}
            user_interests = {interest.lower() for interest in session.user_interests}

            overlap = len(feed_hashtags & user_interests)
            if feed_hashtags:
                relevance_score += (overlap / len(feed_hashtags)) * 0.6

        # Check text keyword overlap
        feed_words = set(feed.text.lower().split())
        user_interests_words = {word.lower() for interest in session.user_interests for word in interest.split()}

        keyword_overlap = len(feed_words & user_interests_words)
        if feed_words:
            relevance_score += (keyword_overlap / len(feed_words)) * 0.4

        return min(relevance_score, 1.0)

    def end_session(self, user_id: str) -> Optional[SessionResult]:
        """
        结束会话
        End user session

        Args:
            user_id: User identifier

        Returns:
            SessionResult if session existed, None otherwise
        """
        if user_id not in self.active_sessions:
            logger.warning(f"No active session for user {user_id}")
            return None

        session = self.active_sessions[user_id]

        # Create final result
        result = SessionResult(
            session=session,
            consumption_log=session.consumed_content,
            total_time_spent_minutes=(datetime.utcnow() - session.session_start).total_seconds() / 60
        )

        self.session_history.append(result)
        del self.active_sessions[user_id]

        logger.info(f"Session ended for user {user_id}")

        return result

    def get_session_analytics(self, user_id: Optional[str] = None) -> Dict:
        """
        获取会话分析
        Get session analytics

        Args:
            user_id: Optional user ID to filter by

        Returns:
            Analytics dictionary
        """
        sessions = [s for s in self.session_history if user_id is None or s.session.user_id == user_id]

        if not sessions:
            return {}

        total_sessions = len(sessions)
        avg_content_viewed = sum(len(s.consumption_log) for s in sessions) / total_sessions
        avg_engagement_rate = sum(s.session.engagement_rate for s in sessions) / total_sessions
        avg_time_spent = sum(s.total_time_spent_minutes for s in sessions) / total_sessions

        return {
            "total_sessions": total_sessions,
            "avg_content_viewed": avg_content_viewed,
            "avg_engagement_rate": avg_engagement_rate,
            "avg_time_spent_minutes": avg_time_spent,
            "user_id": user_id
        }
