"""
Viral Feed - Extended feed model with viral propagation tracking
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime

from ..models.feed import Feed, FeedType
from ..models.entities import Entities
from ..models.metrics import PublicMetrics
from ..models.references import ReferencedFeed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class ViralFeed(Feed):
    """
    病毒传播Feed扩展
    Extended Feed model with viral propagation metrics and tracking
    """

    # 病毒传播特有字段 - Viral-specific fields
    viral_coefficient: Optional[float] = None      # R值 - Viral coefficient
    spread_velocity: Optional[float] = None        # 传播速度 - Spread rate (eng/hour)
    cascade_depth: Optional[int] = None            # 级联深度 - Cascade depth
    influence_reach: Optional[int] = None          # 影响范围 - Total reach estimate
    viral_triggers: List[str] = field(default_factory=list)  # 病毒触发因素

    # 传播路径 - Propagation tracking
    propagation_path: List[str] = field(default_factory=list)  # Path of user IDs
    amplification_nodes: List[str] = field(default_factory=list)  # Key amplifiers

    # 趋势相关 - Trend alignment
    trend_alignment_score: Optional[float] = None   # Alignment with trends (0-1)
    trend_acceleration_factor: Optional[float] = None  # Trend boost factor

    # 生命周期追踪 - Lifecycle tracking
    peak_engagement_time: Optional[str] = None      # Peak timestamp
    virality_phase: str = "emerging"                # emerging, growth, peak, decline, tail

    def calculate_virality_score(self) -> float:
        """
        计算综合病毒性评分
        Calculate composite virality score (0-1)

        Weighted combination of:
        - Viral coefficient (40%)
        - Spread velocity (30%)
        - Cascade depth (20%)
        - Trend alignment (10%)
        """
        logger.debug(f"Calculating virality score for {self.id}")

        try:
            if not self.viral_coefficient or not self.spread_velocity:
                return 0.0

            # Normalize components to 0-1 scale
            # Viral coefficient: 0.5 = 0, 1.0 = 0.5, 2.0+ = 1.0
            vc_normalized = min((self.viral_coefficient - 0.5) / 1.5, 1.0) if self.viral_coefficient > 0.5 else 0.0

            # Spread velocity: normalize by expected max (e.g., 100 eng/hour)
            sv_normalized = min(self.spread_velocity / 100, 1.0)

            # Cascade depth: normalize by expected max (e.g., depth 10)
            cd_normalized = min((self.cascade_depth or 0) / 10, 1.0)

            # Trend alignment: already 0-1
            ta_normalized = self.trend_alignment_score or 0.0

            score = (
                vc_normalized * 0.4 +
                sv_normalized * 0.3 +
                cd_normalized * 0.2 +
                ta_normalized * 0.1
            )

            logger.debug(
                f"Virality score for {self.id}: {score:.3f}",
                vc=vc_normalized,
                sv=sv_normalized,
                cd=cd_normalized,
                ta=ta_normalized
            )

            return min(score, 1.0)

        except Exception as e:
            logger.error(f"Error calculating virality score for {self.id}", exception=e)
            return 0.0

    def is_viral(self, threshold: float = 0.7) -> bool:
        """
        判断是否为病毒内容
        Determine if content is viral based on threshold

        Args:
            threshold: Virality score threshold (default: 0.7)

        Returns:
            True if content is viral
        """
        score = self.calculate_virality_score()
        is_viral = score >= threshold

        logger.info(
            f"Viral check for {self.id}",
            score=score,
            threshold=threshold,
            is_viral=is_viral
        )

        return is_viral

    def update_virality_phase(self):
        """
        更新病毒传播阶段
        Update virality phase based on current metrics
        """
        score = self.calculate_virality_score()

        if score < 0.2:
            self.virality_phase = "emerging"
        elif score < 0.5:
            self.virality_phase = "growth"
        elif score < 0.8:
            self.virality_phase = "peak"
        elif score < 0.4:
            self.virality_phase = "decline"
        else:
            self.virality_phase = "tail"

        logger.debug(f"Updated virality phase for {self.id}: {self.virality_phase}")

    def add_propagation_node(self, user_id: str, is_amplifier: bool = False):
        """
        添加传播节点
        Add user to propagation path

        Args:
            user_id: User who shared/amplified content
            is_amplifier: Whether user significantly amplified reach
        """
        if user_id not in self.propagation_path:
            self.propagation_path.append(user_id)

        if is_amplifier and user_id not in self.amplification_nodes:
            self.amplification_nodes.append(user_id)

        logger.debug(
            f"Added propagation node to {self.id}",
            user_id=user_id,
            is_amplifier=is_amplifier
        )

    def get_propagation_stats(self) -> Dict[str, Any]:
        """
        获取传播统计
        Get propagation statistics

        Returns:
            Dictionary with propagation stats
        """
        return {
            "total_propagators": len(self.propagation_path),
            "key_amplifiers": len(self.amplification_nodes),
            "cascade_depth": self.cascade_depth or 0,
            "influence_reach": self.influence_reach or 0,
            "virality_score": self.calculate_virality_score(),
            "virality_phase": self.virality_phase
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典 (扩展父类方法)
        Convert to dictionary with viral extensions
        """
        # Get base feed dictionary
        base_dict = super().to_dict()

        # Add viral-specific fields
        viral_dict = {
            "viral_coefficient": self.viral_coefficient,
            "spread_velocity": self.spread_velocity,
            "cascade_depth": self.cascade_depth,
            "influence_reach": self.influence_reach,
            "viral_triggers": self.viral_triggers,
            "propagation_path": self.propagation_path,
            "amplification_nodes": self.amplification_nodes,
            "trend_alignment_score": self.trend_alignment_score,
            "trend_acceleration_factor": self.trend_acceleration_factor,
            "peak_engagement_time": self.peak_engagement_time,
            "virality_phase": self.virality_phase,
            "virality_score": self.calculate_virality_score(),
            "is_viral": self.is_viral()
        }

        # Merge dictionaries
        base_dict.update({k: v for k, v in viral_dict.items() if v is not None})

        return base_dict

    @classmethod
    def from_feed(cls, feed: Feed, **viral_kwargs) -> 'ViralFeed':
        """
        从普通Feed创建ViralFeed
        Create ViralFeed from regular Feed

        Args:
            feed: Base Feed object
            **viral_kwargs: Viral-specific parameters

        Returns:
            ViralFeed instance
        """
        # Extract all Feed attributes
        feed_dict = {
            'id': feed.id,
            'text': feed.text,
            'author_id': feed.author_id,
            'created_at': feed.created_at,
            'feed_type': feed.feed_type,
            'conversation_id': feed.conversation_id,
            'in_reply_to_user_id': feed.in_reply_to_user_id,
            'referenced_feeds': feed.referenced_feeds,
            'entities': feed.entities,
            'public_metrics': feed.public_metrics,
            'lang': feed.lang,
            'source': feed.source,
            'possibly_sensitive': feed.possibly_sensitive,
            'platform': feed.platform
        }

        # Merge with viral-specific fields
        feed_dict.update(viral_kwargs)

        return cls(**feed_dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ViralFeed':
        """
        从字典创建ViralFeed
        Create ViralFeed from dictionary

        Args:
            data: Dictionary with feed and viral data

        Returns:
            ViralFeed instance
        """
        from ..models.entities import Entities, HashtagEntity, MentionEntity, UrlEntity
        from ..models.metrics import PublicMetrics
        from ..models.references import ReferencedFeed

        # Convert string feed_type to enum
        if 'feed_type' in data and isinstance(data['feed_type'], str):
            data['feed_type'] = FeedType(data['feed_type'])

        # Convert entities
        if data.get('entities'):
            entities_data = data['entities']
            data['entities'] = Entities(
                hashtags=[HashtagEntity(**h) for h in entities_data.get('hashtags', [])],
                mentions=[MentionEntity(**m) for m in entities_data.get('mentions', [])],
                urls=[UrlEntity(**u) for u in entities_data.get('urls', [])]
            )

        # Convert other complex fields
        if data.get('referenced_feeds'):
            data['referenced_feeds'] = [ReferencedFeed(**rf) for rf in data['referenced_feeds']]

        if data.get('public_metrics'):
            data['public_metrics'] = PublicMetrics(**data['public_metrics'])

        return cls(**data)
