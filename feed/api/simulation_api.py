"""
Feed Simulation API - Main API for Arena, Agent and other system integration
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import timedelta
from pathlib import Path

from ..utils.simulation_manager import SimulationFeedManager, SimulationConfig
from ..models.feed import Feed, FeedType
from ..feed_extensions.viral_feed import ViralFeed
from ..feed_extensions.sponsored_feed import SponsoredFeed
from ..simulation.viral_metrics import ViralContext
from ..simulation.trend_decay_model import TrendShock, TrendLifecycle
from ..simulation.session_manager import SessionParams, SessionResult
from ..governance.safety_filter import SafetyFilter, SafetyConfig
from ..governance.fairness_monitor import FairnessMonitor, FairnessReport
from ..governance.brand_safety import BrandSafety, BrandSafetyConfig, BrandContext
from ..analytics.virality_analyzer import ViralityAnalyzer
from ..analytics.influence_tracker import InfluenceTracker
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class GovernanceFilterConfig:
    """治理过滤配置 - Governance filter configuration"""
    enable_safety_filter: bool = True
    enable_fairness_check: bool = True
    enable_brand_safety: bool = True
    safety_threshold: float = 0.7
    brand_context: Optional[BrandContext] = None

    def to_dict(self) -> Dict:
        return {
            "enable_safety_filter": self.enable_safety_filter,
            "enable_fairness_check": self.enable_fairness_check,
            "enable_brand_safety": self.enable_brand_safety,
            "safety_threshold": self.safety_threshold,
            "brand_context": self.brand_context.to_dict() if self.brand_context else None
        }


class FeedSimulationAPI:
    """
    Feed仿真API - Main API for integration with other systems

    Provides high-level interface for:
    - Viral content simulation
    - Trend injection and modeling
    - Content governance
    - Analytics and insights
    """

    def __init__(
        self,
        storage_dir: str = "./feeds",
        trace_dir: str = "./trace",
        simulation_config: Optional[SimulationConfig] = None
    ):
        """
        Initialize Feed Simulation API

        Args:
            storage_dir: Directory for feed storage
            trace_dir: Directory for trace logs
            simulation_config: Simulation configuration
        """
        self.manager = SimulationFeedManager(storage_dir, simulation_config)
        self.trace_dir = Path(trace_dir)

        # Initialize governance components
        self.safety_filter = SafetyFilter()
        self.fairness_monitor = FairnessMonitor()
        self.brand_safety = BrandSafety()

        # Initialize analytics
        self.virality_analyzer = ViralityAnalyzer()
        self.influence_tracker = InfluenceTracker()

        logger.info(
            "FeedSimulationAPI initialized",
            storage_dir=storage_dir,
            trace_dir=trace_dir
        )

    @logger.trace_decorator
    async def inject_trend_shock(
        self,
        trend_name: str,
        intensity: float,
        duration_hours: float = 6.0
    ) -> Dict:
        """
        注入趋势冲击
        Inject trend shock into simulation

        Args:
            trend_name: Trend name/hashtag
            intensity: Shock intensity (0-1)
            duration_hours: Duration in hours

        Returns:
            Dictionary with shock results
        """
        logger.info(
            f"API: Injecting trend shock",
            trend=trend_name,
            intensity=intensity
        )

        try:
            shock = self.manager.inject_trend_shock(
                trend_name,
                intensity,
                duration_hours
            )

            return shock.to_dict()

        except Exception as e:
            logger.error(f"API: Error injecting trend shock", exception=e)
            raise

    @logger.trace_decorator
    async def get_viral_content(
        self,
        virality_threshold: float = 0.7,
        limit: int = 100,
        apply_governance: bool = True
    ) -> List[Dict]:
        """
        获取病毒内容
        Get viral content with optional governance filters

        Args:
            virality_threshold: Minimum virality score
            limit: Maximum results
            apply_governance: Apply governance filters

        Returns:
            List of viral feed dictionaries
        """
        logger.info(
            f"API: Getting viral content",
            threshold=virality_threshold,
            limit=limit
        )

        try:
            viral_feeds = self.manager.get_viral_content(virality_threshold, limit)

            # Apply governance if requested
            if apply_governance and viral_feeds:
                viral_feeds = self.safety_filter.filter_unsafe_content(viral_feeds)

            # Convert to dictionaries
            result = [feed.to_dict() for feed in viral_feeds]

            logger.info(f"API: Returned {len(result)} viral feeds")

            return result

        except Exception as e:
            logger.error("API: Error getting viral content", exception=e)
            return []

    @logger.trace_decorator
    async def simulate_content_lifecycle(
        self,
        feed_id: str,
        simulation_duration: timedelta,
        initial_exposure: int = 1000
    ) -> Dict:
        """
        模拟内容生命周期
        Simulate complete content lifecycle

        Args:
            feed_id: Feed identifier
            simulation_duration: Duration to simulate
            initial_exposure: Initial exposure count

        Returns:
            Dictionary with lifecycle data
        """
        logger.info(
            f"API: Simulating lifecycle for feed {feed_id}",
            duration_hours=simulation_duration.total_seconds() / 3600
        )

        try:
            # Load feed
            feeds = self.manager.load_all_feeds()
            feed = next((f for f in feeds if f.id == feed_id), None)

            if not feed:
                logger.warning(f"Feed {feed_id} not found")
                return {"error": "Feed not found"}

            # Simulate engagement
            duration_hours = int(simulation_duration.total_seconds() / 3600)
            engagement_wave = await self.manager.simulate_feed_engagement(
                feed,
                initial_exposure,
                duration_hours
            )

            # Calculate virality metrics
            virality = self.manager.calculate_feed_virality(feed)

            # Combine results
            result = {
                "feed_id": feed_id,
                "engagement_wave": engagement_wave.to_dict(),
                "virality_metrics": virality,
                "simulation_duration_hours": duration_hours
            }

            logger.info(f"API: Lifecycle simulation completed for {feed_id}")

            return result

        except Exception as e:
            logger.error(f"API: Error simulating lifecycle for {feed_id}", exception=e)
            return {"error": str(e)}

    @logger.trace_decorator
    async def apply_governance_filters(
        self,
        feeds: List[Feed],
        filter_config: GovernanceFilterConfig
    ) -> List[Feed]:
        """
        应用治理过滤器
        Apply governance filters to content

        Args:
            feeds: List of feeds to filter
            filter_config: Filter configuration

        Returns:
            List of approved feeds
        """
        logger.info(
            f"API: Applying governance filters to {len(feeds)} feeds"
        )

        try:
            filtered_feeds = feeds

            # Safety filter
            if filter_config.enable_safety_filter:
                filtered_feeds = self.safety_filter.filter_unsafe_content(
                    filtered_feeds,
                    filter_config.safety_threshold
                )
                logger.info(f"After safety filter: {len(filtered_feeds)} feeds")

            # Brand safety filter
            if filter_config.enable_brand_safety and filter_config.brand_context:
                filtered_feeds = self.brand_safety.create_brand_safe_feed_collection(
                    filtered_feeds,
                    filter_config.brand_context
                )
                logger.info(f"After brand safety: {len(filtered_feeds)} feeds")

            logger.info(
                f"API: Governance filtering completed",
                original_count=len(feeds),
                filtered_count=len(filtered_feeds)
            )

            return filtered_feeds

        except Exception as e:
            logger.error("API: Error applying governance filters", exception=e)
            return feeds

    @logger.trace_decorator
    async def analyze_viral_patterns(
        self,
        min_virality_score: float = 0.7
    ) -> Dict:
        """
        分析病毒模式
        Analyze patterns in viral content

        Args:
            min_virality_score: Minimum virality score

        Returns:
            Dictionary with pattern analysis
        """
        logger.info(f"API: Analyzing viral patterns")

        try:
            # Get viral content
            viral_feeds = self.manager.get_viral_content(min_virality_score)

            if not viral_feeds:
                return {"error": "No viral content found"}

            # Analyze patterns
            patterns = self.virality_analyzer.analyze_viral_content_patterns(viral_feeds)

            logger.info("API: Viral pattern analysis completed")

            return patterns.to_dict()

        except Exception as e:
            logger.error("API: Error analyzing viral patterns", exception=e)
            return {"error": str(e)}

    @logger.trace_decorator
    async def track_user_influence(
        self,
        user_id: str,
        time_window_days: int = 30
    ) -> Dict:
        """
        追踪用户影响力
        Track user's influence evolution

        Args:
            user_id: User identifier
            time_window_days: Time window in days

        Returns:
            Dictionary with influence data
        """
        logger.info(f"API: Tracking influence for user {user_id}")

        try:
            # Get user's content
            user_feeds = self.manager.search_feeds(author_id=user_id)

            if not user_feeds:
                return {"error": "No content found for user"}

            # Track influence evolution
            evolution = self.influence_tracker.track_user_influence_evolution(
                user_id,
                user_feeds
            )

            logger.info(f"API: Influence tracking completed for {user_id}")

            return evolution.to_dict()

        except Exception as e:
            logger.error(f"API: Error tracking influence for {user_id}", exception=e)
            return {"error": str(e)}

    @logger.trace_decorator
    async def create_sponsored_campaign(
        self,
        text: str,
        author_id: str,
        sponsor_brand: str,
        campaign_id: str,
        budget: float,
        target_ctr: float = 0.03
    ) -> Dict:
        """
        创建赞助活动
        Create sponsored content campaign

        Args:
            text: Content text
            author_id: Author ID
            sponsor_brand: Sponsor brand name
            campaign_id: Campaign ID
            budget: Campaign budget
            target_ctr: Target CTR

        Returns:
            Dictionary with sponsored feed data
        """
        logger.info(
            f"API: Creating sponsored campaign",
            sponsor=sponsor_brand,
            campaign=campaign_id
        )

        try:
            sponsored_feed = self.manager.create_sponsored_feed(
                text=text,
                author_id=author_id,
                sponsor_brand=sponsor_brand,
                campaign_id=campaign_id,
                sponsored_params={
                    "budget_allocated": budget,
                    "ctr_target": target_ctr
                }
            )

            # Save feed
            self.manager.save_feed(sponsored_feed)

            logger.info(f"API: Sponsored campaign created: {sponsored_feed.id}")

            return sponsored_feed.to_dict()

        except Exception as e:
            logger.error("API: Error creating sponsored campaign", exception=e)
            return {"error": str(e)}

    @logger.trace_decorator
    async def get_simulation_status(self) -> Dict:
        """
        获取仿真状态
        Get current simulation status

        Returns:
            Dictionary with simulation status
        """
        logger.info("API: Getting simulation status")

        try:
            stats = self.manager.get_simulation_stats()

            logger.info("API: Simulation status retrieved")

            return stats

        except Exception as e:
            logger.error("API: Error getting simulation status", exception=e)
            return {"error": str(e)}

    @logger.trace_decorator
    async def create_viral_feed(
        self,
        text: str,
        author_id: str,
        viral_coefficient: Optional[float] = None,
        trend_tags: Optional[List[str]] = None
    ) -> Dict:
        """
        创建病毒Feed
        Create viral feed with tracking

        Args:
            text: Content text
            author_id: Author ID
            viral_coefficient: Optional viral coefficient
            trend_tags: Optional trend tags

        Returns:
            Dictionary with viral feed data
        """
        logger.info(f"API: Creating viral feed for author {author_id}")

        try:
            viral_params = {}
            if viral_coefficient:
                viral_params["viral_coefficient"] = viral_coefficient
            if trend_tags:
                viral_params["viral_triggers"] = trend_tags

            viral_feed = self.manager.create_viral_feed(
                text=text,
                author_id=author_id,
                viral_params=viral_params
            )

            # Save feed
            self.manager.save_feed(viral_feed)

            logger.info(f"API: Viral feed created: {viral_feed.id}")

            return viral_feed.to_dict()

        except Exception as e:
            logger.error("API: Error creating viral feed", exception=e)
            return {"error": str(e)}
