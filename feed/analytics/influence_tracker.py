"""
Influence Tracker - Track user and content influence propagation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class InfluencePoint:
    """影响力点 - Single influence measurement point"""
    timestamp: datetime
    content_id: str
    influence_score: float
    reach: int
    engagement_quality: float

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "content_id": self.content_id,
            "influence_score": self.influence_score,
            "reach": self.reach,
            "engagement_quality": self.engagement_quality
        }


@dataclass
class InfluenceEvolution:
    """影响力演化 - User's influence evolution over time"""
    user_id: str
    trajectory: List[InfluencePoint] = field(default_factory=list)
    peak_influence: float = 0.0
    current_influence: float = 0.0
    trend: str = "stable"  # "growing", "declining", "stable"

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "trajectory": [p.to_dict() for p in self.trajectory],
            "peak_influence": self.peak_influence,
            "current_influence": self.current_influence,
            "trend": self.trend
        }


@dataclass
class InfluenceNode:
    """影响力节点 - Node in influence network"""
    user_id: str
    influence_score: float
    connections: List[str] = field(default_factory=list)
    depth: int = 0

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "influence_score": self.influence_score,
            "connections": self.connections,
            "depth": self.depth
        }


@dataclass
class InfluenceNetwork:
    """影响力网络 - Network of influence propagation"""
    root_content_id: str
    nodes: List[InfluenceNode] = field(default_factory=list)
    total_reach: int = 0
    max_depth: int = 0

    def to_dict(self) -> Dict:
        return {
            "root_content_id": self.root_content_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "total_reach": self.total_reach,
            "max_depth": self.max_depth
        }


@dataclass
class InfluenceAmplifier:
    """影响力放大器 - Key amplifier in propagation"""
    user_id: str
    amplification_factor: float
    reach_contribution: int
    engagement_contribution: int

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "amplification_factor": self.amplification_factor,
            "reach_contribution": self.reach_contribution,
            "engagement_contribution": self.engagement_contribution
        }


class InfluenceTracker:
    """影响力追踪器 - Track influence propagation"""

    def __init__(self):
        """Initialize influence tracker"""
        self.user_feeds_cache: Dict[str, List[Feed]] = {}
        logger.info("InfluenceTracker initialized")

    @logger.trace_decorator
    def track_user_influence_evolution(
        self,
        user_id: str,
        user_content: List[Feed],
        time_window: Optional[timedelta] = None
    ) -> InfluenceEvolution:
        """
        追踪用户影响力演化
        Track user's influence evolution over time

        Args:
            user_id: User identifier
            user_content: User's content
            time_window: Optional time window

        Returns:
            InfluenceEvolution object
        """
        logger.info(f"Tracking influence evolution for user {user_id}")

        try:
            evolution = InfluenceEvolution(user_id=user_id)

            # Sort content by creation time
            sorted_content = sorted(
                user_content,
                key=lambda f: f.created_at
            )

            influence_points = []

            for feed in sorted_content:
                influence_point = InfluencePoint(
                    timestamp=datetime.fromisoformat(feed.created_at.rstrip('Z')),
                    content_id=feed.id,
                    influence_score=self._calculate_content_influence(feed),
                    reach=self._calculate_content_reach(feed),
                    engagement_quality=self._calculate_engagement_quality(feed)
                )
                influence_points.append(influence_point)

            evolution.trajectory = influence_points

            # Calculate peak and current influence
            if influence_points:
                evolution.peak_influence = max(p.influence_score for p in influence_points)
                evolution.current_influence = influence_points[-1].influence_score

                # Determine trend
                if len(influence_points) >= 3:
                    recent_avg = sum(p.influence_score for p in influence_points[-3:]) / 3
                    earlier_avg = sum(p.influence_score for p in influence_points[:3]) / 3

                    if recent_avg > earlier_avg * 1.2:
                        evolution.trend = "growing"
                    elif recent_avg < earlier_avg * 0.8:
                        evolution.trend = "declining"
                    else:
                        evolution.trend = "stable"

            logger.info(
                f"Influence evolution tracked for {user_id}",
                peak=evolution.peak_influence,
                current=evolution.current_influence,
                trend=evolution.trend
            )

            return evolution

        except Exception as e:
            logger.error(f"Error tracking influence for {user_id}", exception=e)
            return InfluenceEvolution(user_id=user_id)

    def _calculate_content_influence(self, feed: Feed) -> float:
        """Calculate influence score for content"""
        # Weighted combination of engagement metrics
        engagement = (
            feed.public_metrics.like_count * 1.0 +
            feed.public_metrics.retweet_count * 3.0 +  # Shares more valuable
            feed.public_metrics.quote_count * 4.0 +    # Quotes even more valuable
            feed.public_metrics.reply_count * 2.0
        )

        # Normalize to 0-1 scale (log scale for large numbers)
        import math
        influence = math.log10(engagement + 1) / 6  # log10(1M) ≈ 6

        return min(influence, 1.0)

    def _calculate_content_reach(self, feed: Feed) -> int:
        """Calculate estimated reach"""
        if feed.public_metrics.impression_count:
            return feed.public_metrics.impression_count

        # Estimate from engagement (assume 2% engagement rate)
        total_engagement = (
            feed.public_metrics.like_count +
            feed.public_metrics.retweet_count +
            feed.public_metrics.quote_count +
            feed.public_metrics.reply_count
        )

        estimated_reach = int(total_engagement / 0.02) if total_engagement > 0 else 0

        return max(estimated_reach, 100)

    def _calculate_engagement_quality(self, feed: Feed) -> float:
        """Calculate engagement quality score"""
        total_engagement = (
            feed.public_metrics.like_count +
            feed.public_metrics.retweet_count +
            feed.public_metrics.quote_count +
            feed.public_metrics.reply_count
        )

        if total_engagement == 0:
            return 0.0

        # Quality based on engagement type distribution
        # Higher quality = more quotes and replies (deeper engagement)
        deep_engagement = (
            feed.public_metrics.quote_count +
            feed.public_metrics.reply_count
        )

        quality = deep_engagement / total_engagement

        return min(quality, 1.0)

    @logger.trace_decorator
    def analyze_influence_network(
        self,
        root_feed: Feed,
        related_feeds: Optional[List[Feed]] = None
    ) -> InfluenceNetwork:
        """
        分析影响力网络
        Analyze influence propagation network

        Args:
            root_feed: Original feed
            related_feeds: Related/derived feeds

        Returns:
            InfluenceNetwork object
        """
        logger.info(f"Analyzing influence network for feed {root_feed.id}")

        try:
            network = InfluenceNetwork(root_content_id=root_feed.id)

            # Root node
            root_node = InfluenceNode(
                user_id=root_feed.author_id,
                influence_score=self._calculate_content_influence(root_feed),
                depth=0
            )

            network.nodes.append(root_node)
            network.total_reach = self._calculate_content_reach(root_feed)

            # Add related feeds as network nodes
            if related_feeds:
                for i, feed in enumerate(related_feeds[:20]):  # Limit to 20 for performance
                    node = InfluenceNode(
                        user_id=feed.author_id,
                        influence_score=self._calculate_content_influence(feed),
                        connections=[root_feed.author_id],
                        depth=1
                    )

                    network.nodes.append(node)
                    network.total_reach += self._calculate_content_reach(feed)

                network.max_depth = 1

            logger.info(
                f"Influence network analyzed for {root_feed.id}",
                nodes=len(network.nodes),
                total_reach=network.total_reach
            )

            return network

        except Exception as e:
            logger.error(f"Error analyzing influence network for {root_feed.id}", exception=e)
            return InfluenceNetwork(root_content_id=root_feed.id)

    @logger.trace_decorator
    def identify_influence_amplifiers(
        self,
        root_feed: Feed,
        derived_feeds: List[Feed]
    ) -> List[InfluenceAmplifier]:
        """
        识别影响力放大器
        Identify key amplifiers in propagation

        Args:
            root_feed: Original content
            derived_feeds: Derived content (retweets, quotes)

        Returns:
            List of InfluenceAmplifier objects
        """
        logger.info(f"Identifying amplifiers for feed {root_feed.id}")

        try:
            amplifiers = []

            # Group by author
            author_contributions: Dict[str, Dict] = {}

            for feed in derived_feeds:
                author = feed.author_id

                if author not in author_contributions:
                    author_contributions[author] = {
                        "reach": 0,
                        "engagement": 0,
                        "count": 0
                    }

                contrib = author_contributions[author]
                contrib["reach"] += self._calculate_content_reach(feed)
                contrib["engagement"] += (
                    feed.public_metrics.like_count +
                    feed.public_metrics.retweet_count +
                    feed.public_metrics.reply_count
                )
                contrib["count"] += 1

            # Calculate amplification factors
            root_reach = self._calculate_content_reach(root_feed)

            for author, contrib in author_contributions.items():
                if contrib["reach"] > root_reach * 0.1:  # At least 10% of root reach
                    amplifier = InfluenceAmplifier(
                        user_id=author,
                        amplification_factor=contrib["reach"] / max(root_reach, 1),
                        reach_contribution=contrib["reach"],
                        engagement_contribution=contrib["engagement"]
                    )
                    amplifiers.append(amplifier)

            # Sort by amplification factor
            amplifiers.sort(key=lambda a: a.amplification_factor, reverse=True)

            logger.info(
                f"Identified {len(amplifiers)} amplifiers for {root_feed.id}"
            )

            return amplifiers[:10]  # Return top 10

        except Exception as e:
            logger.error(f"Error identifying amplifiers for {root_feed.id}", exception=e)
            return []
