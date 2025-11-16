"""
Engagement Simulator - Simulate realistic user engagement patterns
"""

import random
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from ..models.feed import Feed
from ..models.user import User
from .viral_metrics import EngagementEvent
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class EngagementConfig:
    """互动仿真配置 - Configuration for engagement simulation"""
    simulation_duration: int = 72  # Hours to simulate
    base_engagement_rate: float = 0.03  # 3% base engagement
    viral_threshold: float = 0.7  # Viral coefficient threshold
    decay_rate: float = 0.1  # Hourly decay rate
    time_step_hours: float = 1.0  # Simulation time step

    def to_dict(self) -> Dict:
        return {
            "simulation_duration": self.simulation_duration,
            "base_engagement_rate": self.base_engagement_rate,
            "viral_threshold": self.viral_threshold,
            "decay_rate": self.decay_rate,
            "time_step_hours": self.time_step_hours
        }


@dataclass
class TimeStepEngagement:
    """单个时间步的互动 - Engagement at a specific time step"""
    time_step: int
    timestamp: datetime
    exposure: int
    likes: int
    retweets: int
    quotes: int
    replies: int
    total_engagement: int

    def to_dict(self) -> Dict:
        return {
            "time_step": self.time_step,
            "timestamp": self.timestamp.isoformat(),
            "exposure": self.exposure,
            "likes": self.likes,
            "retweets": self.retweets,
            "quotes": self.quotes,
            "replies": self.replies,
            "total_engagement": self.total_engagement
        }


@dataclass
class EngagementWave:
    """互动波 - Wave of engagement over time"""
    phases: List[TimeStepEngagement] = field(default_factory=list)
    total_exposure: int = 0
    total_engagement: int = 0
    peak_time: Optional[datetime] = None
    peak_engagement: int = 0

    def to_dict(self) -> Dict:
        return {
            "phases": [p.to_dict() for p in self.phases],
            "total_exposure": self.total_exposure,
            "total_engagement": self.total_engagement,
            "peak_time": self.peak_time.isoformat() if self.peak_time else None,
            "peak_engagement": self.peak_engagement
        }


@dataclass
class UserBehaviorModel:
    """用户行为模型 - Model of user engagement behavior"""
    engagement_probability: float = 0.03  # Likelihood to engage
    like_preference: float = 0.7  # Preference for likes vs other actions
    share_threshold: float = 0.8  # Quality threshold for sharing
    reply_threshold: float = 0.6  # Quality threshold for replying
    attention_span: float = 1.0  # Multiplier for attention
    activity_pattern: List[float] = field(default_factory=lambda: [1.0] * 24)  # Hourly activity

    def to_dict(self) -> Dict:
        return {
            "engagement_probability": self.engagement_probability,
            "like_preference": self.like_preference,
            "share_threshold": self.share_threshold,
            "reply_threshold": self.reply_threshold,
            "attention_span": self.attention_span,
            "activity_pattern": self.activity_pattern
        }


@dataclass
class UserSession:
    """用户会话 - User content consumption session"""
    user_id: str
    time_budget: float  # Minutes
    attention_span: float
    preferences: Dict[str, float]
    consumed_content: List[str] = field(default_factory=list)
    engagements: List[EngagementEvent] = field(default_factory=list)
    session_start: datetime = field(default_factory=datetime.utcnow)

    @property
    def time_remaining(self) -> float:
        """Calculate remaining session time"""
        elapsed = sum([self._estimate_view_time(feed_id) for feed_id in self.consumed_content])
        return max(0, self.time_budget - elapsed)

    def _estimate_view_time(self, feed_id: str) -> float:
        """Estimate time spent viewing content (seconds)"""
        return 5.0  # Average 5 seconds per feed

    def add_engagement(self, event: EngagementEvent):
        """Add engagement event to session"""
        self.engagements.append(event)

    def update_state(self, feed: Feed, engagement: Optional[EngagementEvent]):
        """Update session state after viewing content"""
        self.consumed_content.append(feed.id)
        if engagement:
            self.engagements.append(engagement)


@dataclass
class SessionEngagement:
    """会话互动摘要 - Summary of session engagement"""
    user_id: str
    total_views: int
    total_engagements: int
    engagement_rate: float
    session_duration_minutes: float
    engagement_breakdown: Dict[str, int]

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "total_views": self.total_views,
            "total_engagements": self.total_engagements,
            "engagement_rate": self.engagement_rate,
            "session_duration_minutes": self.session_duration_minutes,
            "engagement_breakdown": self.engagement_breakdown
        }


class TimeDynamics:
    """时间动力学 - Model time effects on content propagation"""

    def __init__(self):
        logger.info("Initializing TimeDynamics")

    @logger.trace_decorator
    def calculate_time_decay(self, feed: Feed, current_time: datetime) -> float:
        """
        计算时间衰减因子
        Calculate time decay factor for content

        Different content types have different decay curves:
        - News: Fast decay (6h half-life)
        - Viral/Trending: Slow decay (48h half-life)
        - Normal: Medium decay (24h half-life)

        Args:
            feed: Feed object
            current_time: Current simulation time

        Returns:
            Decay factor (0-1)
        """
        try:
            created_at = datetime.fromisoformat(feed.created_at.rstrip('Z'))
            age = current_time - created_at

            # Determine content type and half-life
            text_lower = feed.text.lower()

            if "news" in text_lower or "breaking" in text_lower:
                half_life = timedelta(hours=6)
            elif feed.entities and feed.entities.hashtags:
                # Check for viral hashtags
                hashtags = [tag.tag.lower() for tag in feed.entities.hashtags]
                if any(tag in ["viral", "trending", "breaking"] for tag in hashtags):
                    half_life = timedelta(hours=48)
                else:
                    half_life = timedelta(hours=24)
            else:
                half_life = timedelta(hours=24)

            # Exponential decay
            decay_factor = math.exp(-age.total_seconds() / half_life.total_seconds())

            logger.debug(
                f"Time decay calculated for {feed.id}",
                age_hours=age.total_seconds() / 3600,
                decay_factor=decay_factor,
                half_life_hours=half_life.total_seconds() / 3600
            )

            return decay_factor

        except Exception as e:
            logger.error(f"Error calculating time decay for {feed.id}", exception=e)
            return 0.5  # Default moderate decay

    def get_hourly_activity_multiplier(self, hour: int) -> float:
        """
        获取小时活跃度倍数
        Get activity multiplier for specific hour (0-23)

        Peak hours: 9-11 AM, 1-3 PM, 7-9 PM
        """
        activity_pattern = {
            0: 0.2, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.2,
            6: 0.4, 7: 0.7, 8: 0.9, 9: 1.0, 10: 1.0, 11: 1.0,
            12: 0.8, 13: 1.0, 14: 1.0, 15: 1.0, 16: 0.8, 17: 0.7,
            18: 0.8, 19: 1.0, 20: 1.0, 21: 1.0, 22: 0.7, 23: 0.4
        }
        return activity_pattern.get(hour, 0.5)


class EngagementSimulator:
    """互动仿真器 - Simulator for realistic user engagement"""

    def __init__(self, config: Optional[EngagementConfig] = None):
        """
        Initialize engagement simulator

        Args:
            config: Engagement configuration
        """
        self.config = config or EngagementConfig()
        self.user_behavior_models: Dict[str, UserBehaviorModel] = {}
        self.time_dynamics = TimeDynamics()

        logger.info("EngagementSimulator initialized", config=self.config.to_dict())

    @logger.trace_decorator
    def simulate_engagement_wave(
        self,
        feed: Feed,
        initial_exposure: int
    ) -> EngagementWave:
        """
        模拟互动波
        Simulate wave of engagement over time

        Args:
            feed: Feed to simulate engagement for
            initial_exposure: Initial number of people exposed

        Returns:
            EngagementWave with time-series engagement data
        """
        logger.info(
            f"Simulating engagement wave for {feed.id}",
            initial_exposure=initial_exposure,
            duration=self.config.simulation_duration
        )

        try:
            wave_phases = []
            current_exposure = initial_exposure
            created_at = datetime.fromisoformat(feed.created_at.rstrip('Z'))

            for time_step in range(int(self.config.simulation_duration / self.config.time_step_hours)):
                current_time = created_at + timedelta(hours=time_step * self.config.time_step_hours)

                # Simulate this time step
                engagement = self._simulate_time_step_engagement(
                    feed=feed,
                    exposure=current_exposure,
                    time_step=time_step,
                    current_time=current_time
                )

                wave_phases.append(engagement)

                # Update exposure based on shares (viral propagation)
                current_exposure = self._update_exposure(engagement, current_exposure)

            # Calculate wave statistics
            wave = EngagementWave(phases=wave_phases)
            wave.total_exposure = sum(p.exposure for p in wave_phases)
            wave.total_engagement = sum(p.total_engagement for p in wave_phases)

            # Find peak
            if wave_phases:
                peak_phase = max(wave_phases, key=lambda p: p.total_engagement)
                wave.peak_time = peak_phase.timestamp
                wave.peak_engagement = peak_phase.total_engagement

            logger.info(
                f"Engagement wave completed for {feed.id}",
                total_exposure=wave.total_exposure,
                total_engagement=wave.total_engagement,
                peak_engagement=wave.peak_engagement
            )

            return wave

        except Exception as e:
            logger.error(f"Error simulating engagement wave for {feed.id}", exception=e)
            return EngagementWave()

    def _simulate_time_step_engagement(
        self,
        feed: Feed,
        exposure: int,
        time_step: int,
        current_time: datetime
    ) -> TimeStepEngagement:
        """
        模拟单个时间步的互动
        Simulate engagement for a single time step

        Args:
            feed: Feed object
            exposure: Number of people exposed
            time_step: Current time step
            current_time: Current simulation time

        Returns:
            TimeStepEngagement for this time step
        """
        # Calculate engagement factors
        time_decay = self.time_dynamics.calculate_time_decay(feed, current_time)
        hour_multiplier = self.time_dynamics.get_hourly_activity_multiplier(current_time.hour)

        # Base engagement rate adjusted by factors
        effective_rate = self.config.base_engagement_rate * time_decay * hour_multiplier

        # Calculate content quality multiplier
        content_quality = self._estimate_content_quality(feed)
        effective_rate *= content_quality

        # Simulate engagements
        total_engaged = int(exposure * effective_rate * random.uniform(0.8, 1.2))

        # Distribute across engagement types
        likes = int(total_engaged * 0.7)  # 70% likes
        retweets = int(total_engaged * 0.15)  # 15% retweets
        quotes = int(total_engaged * 0.05)  # 5% quotes
        replies = int(total_engaged * 0.10)  # 10% replies

        engagement = TimeStepEngagement(
            time_step=time_step,
            timestamp=current_time,
            exposure=exposure,
            likes=likes,
            retweets=retweets,
            quotes=quotes,
            replies=replies,
            total_engagement=total_engaged
        )

        logger.debug(
            f"Time step {time_step} engagement",
            feed_id=feed.id,
            exposure=exposure,
            total_engagement=total_engaged,
            time_decay=time_decay,
            hour_multiplier=hour_multiplier
        )

        return engagement

    def _estimate_content_quality(self, feed: Feed) -> float:
        """
        估算内容质量
        Estimate content quality based on current metrics

        Returns:
            Quality multiplier (0.5 - 2.0)
        """
        # Use engagement rate as quality indicator
        total_engagement = (
            feed.public_metrics.like_count +
            feed.public_metrics.retweet_count +
            feed.public_metrics.quote_count +
            feed.public_metrics.reply_count
        )

        impressions = feed.public_metrics.impression_count or 1000

        engagement_rate = total_engagement / impressions

        # Normalize (2% = 1.0, 10% = 2.0)
        quality = 0.5 + (engagement_rate / 0.02)

        return max(0.5, min(quality, 2.0))

    def _update_exposure(
        self,
        engagement: TimeStepEngagement,
        current_exposure: int
    ) -> int:
        """
        更新曝光量
        Update exposure based on viral propagation (shares)

        Each share exposes content to N new people (typically 10-50)
        """
        shares = engagement.retweets + engagement.quotes

        # Each share exposes to average 30 new people
        new_exposure = shares * 30

        # Apply decay to prevent infinite growth
        decay_factor = 1.0 - self.config.decay_rate

        updated_exposure = int((current_exposure + new_exposure) * decay_factor)

        return max(updated_exposure, 100)  # Minimum exposure

    @logger.trace_decorator
    def simulate_user_session_engagement(
        self,
        user: User,
        feed_list: List[Feed],
        session_duration_minutes: float = 30.0
    ) -> SessionEngagement:
        """
        模拟用户会话互动
        Simulate user's content consumption session

        Args:
            user: User object
            feed_list: List of feeds shown to user
            session_duration_minutes: Session duration in minutes

        Returns:
            SessionEngagement summary
        """
        logger.info(
            f"Simulating session for user {user.id}",
            feed_count=len(feed_list),
            duration_minutes=session_duration_minutes
        )

        try:
            # Create user session
            session = UserSession(
                user_id=user.id,
                time_budget=session_duration_minutes,
                attention_span=1.0,
                preferences={}
            )

            engagement_breakdown = {
                "likes": 0,
                "retweets": 0,
                "quotes": 0,
                "replies": 0
            }

            for feed in feed_list:
                if session.time_remaining <= 0:
                    break

                # Simulate single feed engagement
                engagement_event = self._simulate_single_feed_engagement(
                    user=user,
                    feed=feed,
                    session=session
                )

                if engagement_event:
                    session.add_engagement(engagement_event)
                    engagement_breakdown[engagement_event.event_type + "s"] += 1

                session.update_state(feed, engagement_event)

            # Calculate summary
            total_views = len(session.consumed_content)
            total_engagements = len(session.engagements)
            engagement_rate = total_engagements / total_views if total_views > 0 else 0.0

            session_engagement = SessionEngagement(
                user_id=user.id,
                total_views=total_views,
                total_engagements=total_engagements,
                engagement_rate=engagement_rate,
                session_duration_minutes=session_duration_minutes,
                engagement_breakdown=engagement_breakdown
            )

            logger.info(
                f"Session completed for user {user.id}",
                total_views=total_views,
                total_engagements=total_engagements,
                engagement_rate=engagement_rate
            )

            return session_engagement

        except Exception as e:
            logger.error(f"Error simulating session for user {user.id}", exception=e)
            return SessionEngagement(
                user_id=user.id,
                total_views=0,
                total_engagements=0,
                engagement_rate=0.0,
                session_duration_minutes=session_duration_minutes,
                engagement_breakdown={}
            )

    def _simulate_single_feed_engagement(
        self,
        user: User,
        feed: Feed,
        session: UserSession
    ) -> Optional[EngagementEvent]:
        """
        模拟单个Feed的互动
        Simulate engagement with a single feed

        Args:
            user: User object
            feed: Feed object
            session: Current user session

        Returns:
            EngagementEvent if user engaged, None otherwise
        """
        # Get or create user behavior model
        if user.id not in self.user_behavior_models:
            self.user_behavior_models[user.id] = UserBehaviorModel()

        behavior = self.user_behavior_models[user.id]

        # Will user engage?
        if random.random() > behavior.engagement_probability:
            return None

        # Determine engagement type
        rand = random.random()

        if rand < behavior.like_preference:
            event_type = "like"
        elif rand < behavior.like_preference + 0.15:
            event_type = "retweet"
        elif rand < behavior.like_preference + 0.20:
            event_type = "quote"
        else:
            event_type = "reply"

        event = EngagementEvent(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            user_id=user.id,
            feed_id=feed.id,
            depth=0
        )

        return event

    def get_user_behavior_model(self, user_id: str) -> UserBehaviorModel:
        """Get or create user behavior model"""
        if user_id not in self.user_behavior_models:
            self.user_behavior_models[user_id] = UserBehaviorModel()
        return self.user_behavior_models[user_id]

    def set_user_behavior_model(self, user_id: str, model: UserBehaviorModel):
        """Set custom user behavior model"""
        self.user_behavior_models[user_id] = model
        logger.info(f"Set custom behavior model for user {user_id}", model=model.to_dict())
