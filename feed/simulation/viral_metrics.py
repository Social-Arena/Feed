"""
Viral Metrics - Calculate and track viral propagation metrics
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class ViralityMetrics:
    """病毒传播指标 - Virality metrics for content propagation"""
    viral_coefficient: float          # 病毒系数 (R值) - average shares per user
    spread_velocity: float            # 传播速度 - propagation rate per hour
    peak_engagement_time: datetime    # 峰值互动时间 - time of maximum engagement
    cascade_depth: int               # 传播层级深度 - depth of sharing cascade
    influence_reach: int             # 影响触达范围 - total reach estimate

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "viral_coefficient": self.viral_coefficient,
            "spread_velocity": self.spread_velocity,
            "peak_engagement_time": self.peak_engagement_time.isoformat(),
            "cascade_depth": self.cascade_depth,
            "influence_reach": self.influence_reach
        }


@dataclass
class EngagementEvent:
    """单个互动事件 - Single engagement event"""
    timestamp: datetime
    event_type: str  # "like", "retweet", "quote", "reply"
    user_id: str
    feed_id: str
    depth: int = 0  # Cascade depth (0 = original post)

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "user_id": self.user_id,
            "feed_id": self.feed_id,
            "depth": self.depth
        }


@dataclass
class ViralContext:
    """病毒传播上下文 - Context for viral potential prediction"""
    author_follower_count: int = 0
    author_verified: bool = False
    trending_hashtags: List[str] = field(default_factory=list)
    current_trends: List[str] = field(default_factory=list)
    time_of_day: int = 12  # Hour (0-23)
    day_of_week: int = 0  # 0=Monday, 6=Sunday
    network_density: float = 0.5  # How connected the network is

    def to_dict(self) -> Dict:
        return {
            "author_follower_count": self.author_follower_count,
            "author_verified": self.author_verified,
            "trending_hashtags": self.trending_hashtags,
            "current_trends": self.current_trends,
            "time_of_day": self.time_of_day,
            "day_of_week": self.day_of_week,
            "network_density": self.network_density
        }


@dataclass
class ViralPotential:
    """病毒传播潜力 - Viral potential prediction"""
    probability: float               # 成为病毒内容的概率 (0-1)
    estimated_peak_reach: int       # 预估峰值触达
    time_to_peak: timedelta         # 预估达到峰值时间
    confidence_score: float         # 预测置信度 (0-1)
    contributing_factors: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "probability": self.probability,
            "estimated_peak_reach": self.estimated_peak_reach,
            "time_to_peak_hours": self.time_to_peak.total_seconds() / 3600,
            "confidence_score": self.confidence_score,
            "contributing_factors": self.contributing_factors
        }


@dataclass
class ViralCascade:
    """病毒传播级联 - Viral propagation cascade tree"""
    root_feed_id: str
    total_nodes: int
    max_depth: int
    cascade_nodes: List[Dict] = field(default_factory=list)  # Tree structure
    engagement_timeline: List[EngagementEvent] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "root_feed_id": self.root_feed_id,
            "total_nodes": self.total_nodes,
            "max_depth": self.max_depth,
            "cascade_nodes": self.cascade_nodes,
            "engagement_timeline": [e.to_dict() for e in self.engagement_timeline]
        }


class ViralityCalculator:
    """病毒性计算器 - Calculator for virality metrics"""

    def __init__(self):
        logger.info("Initializing ViralityCalculator")
        self.engagement_history: Dict[str, List[EngagementEvent]] = {}

    @logger.trace_decorator
    def calculate_viral_coefficient(
        self,
        feed: Feed,
        time_window: timedelta = timedelta(hours=24)
    ) -> float:
        """
        计算病毒系数 - 平均每个用户传播给多少人
        Calculate viral coefficient - average number of shares per user

        R = (Shares + Quotes) / Original Reach
        If R > 1, content is viral (exponential growth)

        Args:
            feed: Feed object to analyze
            time_window: Time window for calculation

        Returns:
            Viral coefficient (R value)
        """
        logger.debug(f"Calculating viral coefficient for feed {feed.id}")

        try:
            shares = feed.public_metrics.retweet_count + feed.public_metrics.quote_count
            original_reach = self._estimate_original_reach(feed)

            if original_reach == 0:
                logger.warning(f"Zero original reach for feed {feed.id}")
                return 0.0

            viral_coefficient = shares / original_reach

            logger.info(
                f"Viral coefficient calculated for {feed.id}",
                coefficient=viral_coefficient,
                shares=shares,
                original_reach=original_reach
            )

            return viral_coefficient

        except Exception as e:
            logger.error(f"Error calculating viral coefficient for {feed.id}", exception=e)
            return 0.0

    def _estimate_original_reach(self, feed: Feed) -> int:
        """
        估算原始触达 - Estimate initial reach of content

        Based on:
        - Impression count (if available)
        - Author's typical reach
        - Engagement rates
        """
        if feed.public_metrics.impression_count:
            return feed.public_metrics.impression_count

        # Estimate based on engagement
        # Typical engagement rate is 2-5%, so reverse calculate
        total_engagement = (
            feed.public_metrics.like_count +
            feed.public_metrics.reply_count +
            feed.public_metrics.retweet_count +
            feed.public_metrics.quote_count
        )

        # Assume 3% engagement rate
        estimated_reach = int(total_engagement / 0.03) if total_engagement > 0 else 100

        return max(estimated_reach, 100)  # Minimum reach of 100

    @logger.trace_decorator
    def calculate_spread_velocity(
        self,
        feed: Feed,
        engagement_timeline: List[EngagementEvent]
    ) -> float:
        """
        计算传播速度 - 单位时间内的传播增长率
        Calculate spread velocity - engagement growth rate per hour

        Velocity = Total Engagements / Hours Since Creation

        Args:
            feed: Feed object
            engagement_timeline: List of engagement events

        Returns:
            Spread velocity (engagements per hour)
        """
        logger.debug(f"Calculating spread velocity for feed {feed.id}")

        try:
            if not engagement_timeline:
                # Use metrics if no timeline available
                created_at = datetime.fromisoformat(feed.created_at.rstrip('Z'))
                age_hours = (datetime.utcnow() - created_at).total_seconds() / 3600

                if age_hours == 0:
                    return 0.0

                total_engagement = (
                    feed.public_metrics.like_count +
                    feed.public_metrics.retweet_count +
                    feed.public_metrics.quote_count +
                    feed.public_metrics.reply_count
                )

                velocity = total_engagement / age_hours
            else:
                # Calculate from timeline
                time_span = (
                    engagement_timeline[-1].timestamp -
                    engagement_timeline[0].timestamp
                ).total_seconds() / 3600

                if time_span == 0:
                    return 0.0

                velocity = len(engagement_timeline) / time_span

            logger.info(
                f"Spread velocity calculated for {feed.id}",
                velocity=velocity,
                engagement_count=len(engagement_timeline)
            )

            return velocity

        except Exception as e:
            logger.error(f"Error calculating spread velocity for {feed.id}", exception=e)
            return 0.0

    @logger.trace_decorator
    def predict_viral_potential(
        self,
        feed: Feed,
        context: ViralContext
    ) -> ViralPotential:
        """
        预测病毒传播潜力
        Predict viral potential based on content features and context

        Factors:
        1. Content quality (engagement rate)
        2. Author influence (follower count, verified status)
        3. Timing (time of day, day of week)
        4. Trend alignment
        5. Network effects

        Args:
            feed: Feed object
            context: Viral context information

        Returns:
            ViralPotential prediction
        """
        logger.debug(f"Predicting viral potential for feed {feed.id}")

        try:
            factors = {}

            # 1. Content engagement factor
            content_factor = self._calculate_content_factor(feed)
            factors['content_quality'] = content_factor

            # 2. Author influence factor
            influence_factor = self._calculate_influence_factor(context)
            factors['author_influence'] = influence_factor

            # 3. Timing factor
            timing_factor = self._calculate_timing_factor(context)
            factors['timing'] = timing_factor

            # 4. Trend alignment factor
            trend_factor = self._calculate_trend_factor(feed, context)
            factors['trend_alignment'] = trend_factor

            # 5. Network factor
            network_factor = context.network_density
            factors['network_density'] = network_factor

            # Weighted combination
            probability = (
                content_factor * 0.3 +
                influence_factor * 0.25 +
                timing_factor * 0.15 +
                trend_factor * 0.2 +
                network_factor * 0.1
            )

            # Estimate peak reach
            base_reach = context.author_follower_count or 1000
            viral_multiplier = 1 + (probability * 50)  # Can go viral by 50x
            estimated_peak_reach = int(base_reach * viral_multiplier)

            # Estimate time to peak (higher probability = faster peak)
            hours_to_peak = 48 * (1 - probability * 0.5)  # 12-48 hours
            time_to_peak = timedelta(hours=hours_to_peak)

            # Confidence based on data availability
            confidence = min(
                (content_factor + influence_factor + trend_factor) / 3,
                0.95
            )

            potential = ViralPotential(
                probability=probability,
                estimated_peak_reach=estimated_peak_reach,
                time_to_peak=time_to_peak,
                confidence_score=confidence,
                contributing_factors=factors
            )

            logger.info(
                f"Viral potential predicted for {feed.id}",
                probability=probability,
                peak_reach=estimated_peak_reach,
                confidence=confidence
            )

            return potential

        except Exception as e:
            logger.error(f"Error predicting viral potential for {feed.id}", exception=e)
            return ViralPotential(
                probability=0.0,
                estimated_peak_reach=0,
                time_to_peak=timedelta(hours=24),
                confidence_score=0.0
            )

    def _calculate_content_factor(self, feed: Feed) -> float:
        """Calculate content quality factor based on engagement metrics"""
        total_engagement = (
            feed.public_metrics.like_count +
            feed.public_metrics.retweet_count * 2 +  # Shares weighted more
            feed.public_metrics.quote_count * 2 +
            feed.public_metrics.reply_count
        )

        reach = self._estimate_original_reach(feed)
        engagement_rate = total_engagement / max(reach, 1)

        # Normalize to 0-1 scale (5% engagement = 1.0)
        return min(engagement_rate / 0.05, 1.0)

    def _calculate_influence_factor(self, context: ViralContext) -> float:
        """Calculate author influence factor"""
        # Follower count contribution (log scale)
        if context.author_follower_count > 0:
            follower_factor = math.log10(context.author_follower_count) / 7  # 10M followers = 1.0
        else:
            follower_factor = 0.0

        # Verified status bonus
        verified_bonus = 0.2 if context.author_verified else 0.0

        return min(follower_factor + verified_bonus, 1.0)

    def _calculate_timing_factor(self, context: ViralContext) -> float:
        """Calculate timing factor (optimal posting times)"""
        # Peak hours: 9-11 AM, 1-3 PM, 7-9 PM
        hour = context.time_of_day

        if hour in [9, 10, 11, 13, 14, 15, 19, 20, 21]:
            time_score = 1.0
        elif hour in [8, 12, 16, 17, 18, 22]:
            time_score = 0.7
        else:
            time_score = 0.4

        # Weekday vs weekend
        day = context.day_of_week
        day_score = 0.8 if day < 5 else 0.6  # Weekdays better

        return (time_score + day_score) / 2

    def _calculate_trend_factor(self, feed: Feed, context: ViralContext) -> float:
        """Calculate trend alignment factor"""
        if not feed.entities or not feed.entities.hashtags:
            return 0.3  # Base score if no hashtags

        feed_hashtags = {tag.tag.lower() for tag in feed.entities.hashtags}
        trending = {tag.lower() for tag in context.trending_hashtags}

        if not trending:
            return 0.5

        # Calculate overlap
        overlap = len(feed_hashtags & trending) / len(trending)

        return min(overlap + 0.3, 1.0)  # Base 0.3 + overlap bonus

    @logger.trace_decorator
    def track_viral_cascade(
        self,
        original_feed_id: str,
        engagement_events: Optional[List[EngagementEvent]] = None
    ) -> ViralCascade:
        """
        追踪病毒传播级联
        Track viral propagation cascade tree

        Args:
            original_feed_id: ID of original feed
            engagement_events: List of engagement events (optional)

        Returns:
            ViralCascade object with cascade tree
        """
        logger.debug(f"Tracking viral cascade for feed {original_feed_id}")

        try:
            if engagement_events is None:
                engagement_events = self.engagement_history.get(original_feed_id, [])

            # Build cascade tree
            cascade_nodes = []
            max_depth = 0

            # Group by depth
            depth_groups: Dict[int, List[EngagementEvent]] = {}
            for event in engagement_events:
                depth = event.depth
                if depth not in depth_groups:
                    depth_groups[depth] = []
                depth_groups[depth].append(event)
                max_depth = max(max_depth, depth)

            # Build node structure
            for depth in sorted(depth_groups.keys()):
                events = depth_groups[depth]
                cascade_nodes.append({
                    "depth": depth,
                    "node_count": len(events),
                    "events": [e.to_dict() for e in events[:10]]  # Sample first 10
                })

            cascade = ViralCascade(
                root_feed_id=original_feed_id,
                total_nodes=len(engagement_events),
                max_depth=max_depth,
                cascade_nodes=cascade_nodes,
                engagement_timeline=engagement_events
            )

            logger.info(
                f"Viral cascade tracked for {original_feed_id}",
                total_nodes=cascade.total_nodes,
                max_depth=cascade.max_depth
            )

            return cascade

        except Exception as e:
            logger.error(
                f"Error tracking viral cascade for {original_feed_id}",
                exception=e
            )
            return ViralCascade(
                root_feed_id=original_feed_id,
                total_nodes=0,
                max_depth=0
            )

    def add_engagement_event(self, feed_id: str, event: EngagementEvent):
        """Add an engagement event to history"""
        if feed_id not in self.engagement_history:
            self.engagement_history[feed_id] = []

        self.engagement_history[feed_id].append(event)
        logger.debug(
            f"Added engagement event for {feed_id}",
            event_type=event.event_type,
            user_id=event.user_id
        )

    @logger.trace_decorator
    def calculate_complete_metrics(
        self,
        feed: Feed,
        engagement_timeline: Optional[List[EngagementEvent]] = None,
        context: Optional[ViralContext] = None
    ) -> ViralityMetrics:
        """
        计算完整的病毒传播指标
        Calculate complete virality metrics for a feed

        Args:
            feed: Feed object
            engagement_timeline: Optional engagement timeline
            context: Optional viral context

        Returns:
            Complete ViralityMetrics
        """
        logger.info(f"Calculating complete metrics for feed {feed.id}")

        try:
            # Get or create timeline
            if engagement_timeline is None:
                engagement_timeline = self.engagement_history.get(feed.id, [])

            # Calculate metrics
            viral_coefficient = self.calculate_viral_coefficient(feed)
            spread_velocity = self.calculate_spread_velocity(feed, engagement_timeline)

            # Find peak engagement time
            if engagement_timeline:
                # Group by hour and find peak
                hour_counts: Dict[datetime, int] = {}
                for event in engagement_timeline:
                    hour_key = event.timestamp.replace(minute=0, second=0, microsecond=0)
                    hour_counts[hour_key] = hour_counts.get(hour_key, 0) + 1

                peak_time = max(hour_counts.keys(), key=lambda k: hour_counts[k])
            else:
                # Estimate peak time (typically 2-6 hours after posting)
                created_at = datetime.fromisoformat(feed.created_at.rstrip('Z'))
                peak_time = created_at + timedelta(hours=4)

            # Calculate cascade depth
            cascade_depth = max([e.depth for e in engagement_timeline], default=0)

            # Calculate influence reach
            cascade = self.track_viral_cascade(feed.id, engagement_timeline)
            influence_reach = cascade.total_nodes * 10  # Estimate 10 views per engagement

            metrics = ViralityMetrics(
                viral_coefficient=viral_coefficient,
                spread_velocity=spread_velocity,
                peak_engagement_time=peak_time,
                cascade_depth=cascade_depth,
                influence_reach=influence_reach
            )

            logger.info(
                f"Complete metrics calculated for {feed.id}",
                viral_coefficient=viral_coefficient,
                spread_velocity=spread_velocity,
                cascade_depth=cascade_depth
            )

            return metrics

        except Exception as e:
            logger.error(f"Error calculating complete metrics for {feed.id}", exception=e)
            raise
