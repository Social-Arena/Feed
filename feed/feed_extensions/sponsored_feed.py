"""
Sponsored Feed - Extended feed model for sponsored/advertising content
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime

from ..models.feed import Feed, FeedType
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class SponsoredFeed(Feed):
    """
    赞助内容Feed扩展
    Extended Feed model for sponsored/advertising content
    """

    # 赞助信息 - Sponsorship information
    sponsor_brand: Optional[str] = None              # Brand/sponsor name
    campaign_id: Optional[str] = None                # Campaign identifier
    sponsorship_type: str = "paid"                   # "paid", "partnership", "gifted"

    # 商业指标 - Commercial metrics
    ctr_target: Optional[float] = None               # Click-through rate target
    conversion_goal: Optional[str] = None            # Conversion goal type
    budget_allocated: Optional[float] = None         # Budget (USD)
    spend_to_date: float = 0.0                       # Current spend

    # 性能指标 - Performance metrics
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    ctr_actual: Optional[float] = None               # Actual CTR
    cpc: Optional[float] = None                      # Cost per click
    cpa: Optional[float] = None                      # Cost per acquisition

    # 目标受众 - Target audience
    target_demographics: Dict[str, Any] = field(default_factory=dict)
    target_interests: List[str] = field(default_factory=list)
    geo_targeting: List[str] = field(default_factory=list)

    # 透明度 - Transparency
    disclosure_status: str = "disclosed"             # "disclosed", "not_disclosed", "unclear"
    disclosure_text: Optional[str] = None

    def __post_init__(self):
        """确保赞助内容有适当的标识和披露"""
        super().__post_init__()

        # Auto-add disclosure if sponsored
        if self.sponsor_brand and self.disclosure_status == "disclosed":
            self._ensure_disclosure()

    def _ensure_disclosure(self):
        """
        确保披露状态
        Ensure proper disclosure labeling
        """
        disclosure_markers = ["sponsored", "ad", "promoted", "partnership"]

        text_lower = self.text.lower()
        has_disclosure = any(marker in text_lower for marker in disclosure_markers)

        if not has_disclosure:
            # Add disclosure to beginning of text
            disclosure = f"[Sponsored by {self.sponsor_brand}] "
            self.text = disclosure + self.text
            self.disclosure_text = disclosure

            logger.info(
                f"Added disclosure to sponsored feed {self.id}",
                sponsor=self.sponsor_brand
            )

    def update_performance_metrics(
        self,
        impressions: Optional[int] = None,
        clicks: Optional[int] = None,
        conversions: Optional[int] = None
    ):
        """
        更新性能指标
        Update performance metrics

        Args:
            impressions: New impressions count
            clicks: New clicks count
            conversions: New conversions count
        """
        if impressions is not None:
            self.impressions = impressions

        if clicks is not None:
            self.clicks = clicks

        if conversions is not None:
            self.conversions = conversions

        # Calculate derived metrics
        self._calculate_derived_metrics()

        logger.info(
            f"Updated metrics for sponsored feed {self.id}",
            impressions=self.impressions,
            clicks=self.clicks,
            conversions=self.conversions
        )

    def _calculate_derived_metrics(self):
        """
        计算派生指标
        Calculate derived metrics (CTR, CPC, CPA)
        """
        # Calculate CTR
        if self.impressions > 0:
            self.ctr_actual = self.clicks / self.impressions
        else:
            self.ctr_actual = 0.0

        # Calculate CPC
        if self.clicks > 0 and self.spend_to_date > 0:
            self.cpc = self.spend_to_date / self.clicks
        else:
            self.cpc = 0.0

        # Calculate CPA
        if self.conversions > 0 and self.spend_to_date > 0:
            self.cpa = self.spend_to_date / self.conversions
        else:
            self.cpa = 0.0

    def is_meeting_targets(self) -> bool:
        """
        检查是否达到目标
        Check if campaign is meeting performance targets

        Returns:
            True if meeting CTR target
        """
        if self.ctr_target is None or self.ctr_actual is None:
            return False

        return self.ctr_actual >= self.ctr_target

    def get_roi_metrics(self) -> Dict[str, float]:
        """
        获取ROI指标
        Get return on investment metrics

        Returns:
            Dictionary with ROI metrics
        """
        roi_metrics = {
            "ctr": self.ctr_actual or 0.0,
            "cpc": self.cpc or 0.0,
            "cpa": self.cpa or 0.0,
            "total_spend": self.spend_to_date,
            "budget_remaining": (self.budget_allocated or 0) - self.spend_to_date,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "conversions": self.conversions
        }

        # Calculate efficiency score (0-1)
        efficiency = 0.0
        if self.ctr_target and self.ctr_actual:
            efficiency = min(self.ctr_actual / self.ctr_target, 1.0)

        roi_metrics["efficiency_score"] = efficiency

        return roi_metrics

    def update_spend(self, amount: float):
        """
        更新花费
        Update campaign spend

        Args:
            amount: Amount to add to spend
        """
        self.spend_to_date += amount

        if self.budget_allocated and self.spend_to_date >= self.budget_allocated:
            logger.warning(
                f"Budget exceeded for campaign {self.campaign_id}",
                budget=self.budget_allocated,
                spend=self.spend_to_date
            )

    def is_budget_exhausted(self) -> bool:
        """
        检查预算是否用尽
        Check if campaign budget is exhausted

        Returns:
            True if budget is exhausted
        """
        if self.budget_allocated is None:
            return False

        return self.spend_to_date >= self.budget_allocated

    def get_campaign_status(self) -> str:
        """
        获取活动状态
        Get campaign status

        Returns:
            Status string: "active", "budget_exhausted", "underperforming", "meeting_targets"
        """
        if self.is_budget_exhausted():
            return "budget_exhausted"

        if self.is_meeting_targets():
            return "meeting_targets"

        if self.ctr_actual and self.ctr_target and self.ctr_actual < self.ctr_target * 0.5:
            return "underperforming"

        return "active"

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典 (扩展父类方法)
        Convert to dictionary with sponsored extensions
        """
        # Get base feed dictionary
        base_dict = super().to_dict()

        # Add sponsored-specific fields
        sponsored_dict = {
            "sponsor_brand": self.sponsor_brand,
            "campaign_id": self.campaign_id,
            "sponsorship_type": self.sponsorship_type,
            "ctr_target": self.ctr_target,
            "conversion_goal": self.conversion_goal,
            "budget_allocated": self.budget_allocated,
            "spend_to_date": self.spend_to_date,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "conversions": self.conversions,
            "ctr_actual": self.ctr_actual,
            "cpc": self.cpc,
            "cpa": self.cpa,
            "target_demographics": self.target_demographics,
            "target_interests": self.target_interests,
            "geo_targeting": self.geo_targeting,
            "disclosure_status": self.disclosure_status,
            "disclosure_text": self.disclosure_text,
            "roi_metrics": self.get_roi_metrics(),
            "campaign_status": self.get_campaign_status()
        }

        # Merge dictionaries
        base_dict.update({k: v for k, v in sponsored_dict.items() if v is not None or k in ["spend_to_date", "impressions", "clicks", "conversions"]})

        return base_dict

    @classmethod
    def from_feed(cls, feed: Feed, **sponsored_kwargs) -> 'SponsoredFeed':
        """
        从普通Feed创建SponsoredFeed
        Create SponsoredFeed from regular Feed

        Args:
            feed: Base Feed object
            **sponsored_kwargs: Sponsored-specific parameters

        Returns:
            SponsoredFeed instance
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

        # Merge with sponsored-specific fields
        feed_dict.update(sponsored_kwargs)

        return cls(**feed_dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SponsoredFeed':
        """
        从字典创建SponsoredFeed
        Create SponsoredFeed from dictionary

        Args:
            data: Dictionary with feed and sponsored data

        Returns:
            SponsoredFeed instance
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
