"""
Simulation Feed Manager - Extends FeedManager with simulation capabilities
"""

from typing import List, Optional, Dict
from datetime import datetime, timedelta
from pathlib import Path

from .manager import FeedManager
from ..models.feed import Feed, FeedType
from ..feed_extensions.viral_feed import ViralFeed
from ..feed_extensions.sponsored_feed import SponsoredFeed
from ..simulation.viral_metrics import (
    ViralityCalculator,
    ViralContext,
    ViralPotential,
    EngagementEvent
)
from ..simulation.engagement_simulator import (
    EngagementSimulator,
    EngagementConfig,
    EngagementWave
)
from ..simulation.trend_decay_model import (
    TrendDecayModel,
    TrendConfig,
    TrendShock
)
from ..simulation.session_manager import (
    SessionManager,
    SessionConfig,
    SessionParams,
    SessionResult
)
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


class SimulationConfig:
    """仿真配置 - Complete simulation configuration"""

    def __init__(
        self,
        engagement_config: Optional[EngagementConfig] = None,
        trend_config: Optional[TrendConfig] = None,
        session_config: Optional[SessionConfig] = None
    ):
        self.engagement = engagement_config or EngagementConfig()
        self.trend = trend_config or TrendConfig()
        self.session = session_config or SessionConfig()

    def to_dict(self) -> Dict:
        return {
            "engagement": self.engagement.to_dict(),
            "trend": self.trend.to_dict(),
            "session": self.session.to_dict()
        }


class SimulationFeedManager(FeedManager):
    """
    仿真Feed管理器 - Feed manager with simulation capabilities

    Extends FeedManager with:
    - Viral content creation and tracking
    - Engagement simulation
    - Trend modeling
    - Session management
    """

    def __init__(
        self,
        storage_dir: str = "./feeds",
        simulation_config: Optional[SimulationConfig] = None
    ):
        """
        Initialize simulation feed manager

        Args:
            storage_dir: Directory for feed storage
            simulation_config: Simulation configuration
        """
        super().__init__(storage_dir)

        self.simulation_config = simulation_config or SimulationConfig()

        # Initialize simulation components
        self.virality_calculator = ViralityCalculator()
        self.engagement_simulator = EngagementSimulator(self.simulation_config.engagement)
        self.trend_model = TrendDecayModel(self.simulation_config.trend)
        self.session_manager = SessionManager(self.simulation_config.session)

        logger.info(
            "SimulationFeedManager initialized",
            storage_dir=storage_dir,
            config=self.simulation_config.to_dict()
        )

    @logger.trace_decorator
    def create_viral_feed(
        self,
        text: str,
        author_id: str,
        feed_type: FeedType = FeedType.POST,
        viral_params: Optional[Dict] = None,
        **kwargs
    ) -> ViralFeed:
        """
        创建病毒传播Feed
        Create viral propagation feed

        Args:
            text: Feed content
            author_id: Author user ID
            feed_type: Feed type
            viral_params: Viral-specific parameters
            **kwargs: Additional feed parameters

        Returns:
            ViralFeed instance
        """
        logger.info(f"Creating viral feed for author {author_id}")

        try:
            # Create base feed
            base_feed = self.create_feed(text, author_id, feed_type, **kwargs)

            # Convert to ViralFeed
            viral_feed = ViralFeed.from_feed(base_feed, **(viral_params or {}))

            # Initialize virality phase
            viral_feed.update_virality_phase()

            logger.info(
                f"Viral feed created: {viral_feed.id}",
                virality_phase=viral_feed.virality_phase
            )

            return viral_feed

        except Exception as e:
            logger.error(f"Error creating viral feed for author {author_id}", exception=e)
            raise

    @logger.trace_decorator
    def create_sponsored_feed(
        self,
        text: str,
        author_id: str,
        sponsor_brand: str,
        campaign_id: str,
        sponsored_params: Optional[Dict] = None,
        **kwargs
    ) -> SponsoredFeed:
        """
        创建赞助Feed
        Create sponsored feed

        Args:
            text: Feed content
            author_id: Author user ID
            sponsor_brand: Sponsor brand name
            campaign_id: Campaign identifier
            sponsored_params: Sponsored-specific parameters
            **kwargs: Additional feed parameters

        Returns:
            SponsoredFeed instance
        """
        logger.info(
            f"Creating sponsored feed",
            sponsor=sponsor_brand,
            campaign=campaign_id
        )

        try:
            # Create base feed
            base_feed = self.create_feed(text, author_id, **kwargs)

            # Merge sponsored parameters
            params = {
                "sponsor_brand": sponsor_brand,
                "campaign_id": campaign_id,
                **(sponsored_params or {})
            }

            # Convert to SponsoredFeed
            sponsored_feed = SponsoredFeed.from_feed(base_feed, **params)

            logger.info(
                f"Sponsored feed created: {sponsored_feed.id}",
                disclosure_status=sponsored_feed.disclosure_status
            )

            return sponsored_feed

        except Exception as e:
            logger.error(
                f"Error creating sponsored feed",
                sponsor=sponsor_brand,
                exception=e
            )
            raise

    @logger.trace_decorator
    async def simulate_feed_engagement(
        self,
        feed: Feed,
        initial_exposure: int = 1000,
        simulation_duration_hours: Optional[int] = None
    ) -> EngagementWave:
        """
        模拟Feed互动
        Simulate engagement for a feed

        Args:
            feed: Feed to simulate
            initial_exposure: Initial exposure count
            simulation_duration_hours: Override simulation duration

        Returns:
            EngagementWave with simulation results
        """
        logger.info(
            f"Simulating engagement for feed {feed.id}",
            initial_exposure=initial_exposure
        )

        try:
            # Update config if duration specified
            if simulation_duration_hours:
                original_duration = self.simulation_config.engagement.simulation_duration
                self.simulation_config.engagement.simulation_duration = simulation_duration_hours

            # Run simulation
            wave = self.engagement_simulator.simulate_engagement_wave(feed, initial_exposure)

            # Restore original config
            if simulation_duration_hours:
                self.simulation_config.engagement.simulation_duration = original_duration

            logger.info(
                f"Engagement simulation completed for {feed.id}",
                total_engagement=wave.total_engagement,
                peak_engagement=wave.peak_engagement
            )

            return wave

        except Exception as e:
            logger.error(f"Error simulating engagement for {feed.id}", exception=e)
            raise

    @logger.trace_decorator
    def calculate_feed_virality(
        self,
        feed: Feed,
        engagement_timeline: Optional[List[EngagementEvent]] = None,
        context: Optional[ViralContext] = None
    ) -> Dict:
        """
        计算Feed病毒性
        Calculate virality metrics for feed

        Args:
            feed: Feed to analyze
            engagement_timeline: Optional engagement timeline
            context: Optional viral context

        Returns:
            Dictionary with virality metrics
        """
        logger.info(f"Calculating virality for feed {feed.id}")

        try:
            # Calculate viral coefficient
            viral_coefficient = self.virality_calculator.calculate_viral_coefficient(feed)

            # Calculate spread velocity
            spread_velocity = self.virality_calculator.calculate_spread_velocity(
                feed,
                engagement_timeline or []
            )

            # Predict viral potential
            if context is None:
                context = ViralContext()

            viral_potential = self.virality_calculator.predict_viral_potential(feed, context)

            # Track cascade
            cascade = self.virality_calculator.track_viral_cascade(
                feed.id,
                engagement_timeline
            )

            # Calculate complete metrics
            metrics = self.virality_calculator.calculate_complete_metrics(
                feed,
                engagement_timeline,
                context
            )

            result = {
                "viral_coefficient": viral_coefficient,
                "spread_velocity": spread_velocity,
                "viral_potential": viral_potential.to_dict(),
                "cascade": cascade.to_dict(),
                "complete_metrics": metrics.to_dict()
            }

            logger.info(
                f"Virality calculated for {feed.id}",
                viral_coefficient=viral_coefficient,
                spread_velocity=spread_velocity
            )

            return result

        except Exception as e:
            logger.error(f"Error calculating virality for {feed.id}", exception=e)
            raise

    @logger.trace_decorator
    def inject_trend_shock(
        self,
        trend_name: str,
        intensity: float,
        duration_hours: Optional[float] = None
    ) -> TrendShock:
        """
        注入趋势冲击
        Inject trend shock into simulation

        Args:
            trend_name: Name of trend
            intensity: Shock intensity (0-1)
            duration_hours: Duration of shock effect

        Returns:
            TrendShock object
        """
        logger.info(
            f"Injecting trend shock",
            trend=trend_name,
            intensity=intensity
        )

        try:
            # Find affected feeds
            affected_feeds = self.search_feeds(text_contains=trend_name)

            # Apply shock
            duration = timedelta(hours=duration_hours) if duration_hours else None
            shock = self.trend_model.apply_trend_shock(
                trend_name,
                intensity,
                affected_feeds,
                duration
            )

            logger.info(
                f"Trend shock applied",
                trend=trend_name,
                affected_count=len(shock.affected_content)
            )

            return shock

        except Exception as e:
            logger.error(f"Error injecting trend shock for {trend_name}", exception=e)
            raise

    @logger.trace_decorator
    def model_trend_lifecycle(
        self,
        trend: str,
        initial_momentum: float = 10.0
    ) -> Dict:
        """
        建模趋势生命周期
        Model complete trend lifecycle

        Args:
            trend: Trend identifier
            initial_momentum: Initial momentum value

        Returns:
            Dictionary with lifecycle data
        """
        logger.info(f"Modeling lifecycle for trend '{trend}'")

        try:
            lifecycle = self.trend_model.model_trend_lifecycle(trend, initial_momentum)

            logger.info(
                f"Lifecycle modeled for trend '{trend}'",
                peak_momentum=lifecycle.peak_momentum
            )

            return lifecycle.to_dict()

        except Exception as e:
            logger.error(f"Error modeling lifecycle for trend '{trend}'", exception=e)
            raise

    @logger.trace_decorator
    def simulate_user_session(
        self,
        user_id: str,
        available_feeds: List[Feed],
        session_params: Optional[SessionParams] = None
    ) -> SessionResult:
        """
        模拟用户会话
        Simulate user content consumption session

        Args:
            user_id: User identifier
            available_feeds: Feeds to show user
            session_params: Session parameters

        Returns:
            SessionResult with consumption data
        """
        logger.info(
            f"Simulating session for user {user_id}",
            feed_count=len(available_feeds)
        )

        try:
            # Create session
            session = self.session_manager.create_user_session(user_id, session_params)

            # Simulate consumption
            result = self.session_manager.simulate_content_consumption(
                session,
                available_feeds
            )

            logger.info(
                f"Session completed for user {user_id}",
                content_viewed=result.session.content_count,
                engagement_rate=result.session.engagement_rate
            )

            return result

        except Exception as e:
            logger.error(f"Error simulating session for user {user_id}", exception=e)
            raise

    def get_viral_content(
        self,
        virality_threshold: float = 0.7,
        limit: Optional[int] = None
    ) -> List[ViralFeed]:
        """
        获取病毒内容
        Get viral content based on threshold

        Args:
            virality_threshold: Minimum virality score
            limit: Maximum number of results

        Returns:
            List of viral feeds
        """
        logger.info(f"Getting viral content with threshold {virality_threshold}")

        try:
            all_feeds = self.load_all_feeds()
            viral_feeds = []

            for feed in all_feeds:
                # Convert to ViralFeed if needed
                if not isinstance(feed, ViralFeed):
                    viral_feed = ViralFeed.from_feed(feed)
                else:
                    viral_feed = feed

                # Check if viral
                if viral_feed.calculate_virality_score() >= virality_threshold:
                    viral_feeds.append(viral_feed)

            # Sort by virality score
            viral_feeds.sort(
                key=lambda f: f.calculate_virality_score(),
                reverse=True
            )

            # Apply limit
            if limit:
                viral_feeds = viral_feeds[:limit]

            logger.info(f"Found {len(viral_feeds)} viral feeds")

            return viral_feeds

        except Exception as e:
            logger.error("Error getting viral content", exception=e)
            return []

    def get_simulation_stats(self) -> Dict:
        """
        获取仿真统计
        Get simulation statistics

        Returns:
            Dictionary with simulation stats
        """
        return {
            "total_feeds": len(self.load_all_feeds()),
            "active_trends": len(self.trend_model.active_trends),
            "active_sessions": len(self.session_manager.active_sessions),
            "session_history": len(self.session_manager.session_history),
            "config": self.simulation_config.to_dict()
        }
