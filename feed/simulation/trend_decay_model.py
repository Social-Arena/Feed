"""
Trend Decay Model - Model trends lifecycle and decay patterns
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


class TrendPhase(Enum):
    """趋势生命周期阶段 - Trend lifecycle phases"""
    EMERGENCE = "emergence"      # Initial phase, slow growth
    GROWTH = "growth"            # Rapid growth phase
    PEAK = "peak"                # Maximum momentum
    DECLINE = "decline"          # Declining phase
    TAIL = "tail"                # Long tail, residual interest


@dataclass
class TrendConfig:
    """趋势配置 - Trend simulation configuration"""
    emergence_duration_hours: float = 2.0
    growth_duration_hours: float = 6.0
    peak_duration_hours: float = 4.0
    decline_duration_hours: float = 12.0
    tail_duration_hours: float = 48.0

    # Momentum thresholds
    viral_momentum_threshold: float = 100.0
    peak_momentum_threshold: float = 500.0

    def to_dict(self) -> Dict:
        return {
            "emergence_duration_hours": self.emergence_duration_hours,
            "growth_duration_hours": self.growth_duration_hours,
            "peak_duration_hours": self.peak_duration_hours,
            "decline_duration_hours": self.decline_duration_hours,
            "tail_duration_hours": self.tail_duration_hours,
            "viral_momentum_threshold": self.viral_momentum_threshold,
            "peak_momentum_threshold": self.peak_momentum_threshold
        }


@dataclass
class TrendPhaseData:
    """趋势阶段数据 - Data for a specific trend phase"""
    phase: TrendPhase
    start_time: datetime
    end_time: datetime
    duration_hours: float
    momentum_curve: List[float]  # Momentum values over time
    engagement_multiplier: float  # How much this phase boosts engagement

    def to_dict(self) -> Dict:
        return {
            "phase": self.phase.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_hours": self.duration_hours,
            "momentum_curve": self.momentum_curve,
            "engagement_multiplier": self.engagement_multiplier
        }


@dataclass
class TrendLifecycle:
    """趋势生命周期 - Complete trend lifecycle model"""
    trend: str
    phases: List[TrendPhaseData]
    start_time: datetime
    current_phase: TrendPhase = TrendPhase.EMERGENCE
    total_mentions: int = 0
    peak_momentum: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "trend": self.trend,
            "phases": [p.to_dict() for p in self.phases],
            "start_time": self.start_time.isoformat(),
            "current_phase": self.current_phase.value,
            "total_mentions": self.total_mentions,
            "peak_momentum": self.peak_momentum
        }

    def get_current_momentum(self, current_time: datetime) -> float:
        """Get momentum at current time"""
        for phase_data in self.phases:
            if phase_data.start_time <= current_time < phase_data.end_time:
                # Calculate position within phase
                elapsed = (current_time - phase_data.start_time).total_seconds() / 3600
                progress = elapsed / phase_data.duration_hours

                # Interpolate momentum
                if phase_data.momentum_curve:
                    index = int(progress * (len(phase_data.momentum_curve) - 1))
                    return phase_data.momentum_curve[min(index, len(phase_data.momentum_curve) - 1)]

        return 0.0  # Trend ended


@dataclass
class TrendShock:
    """趋势冲击 - Sudden trend shock/spike"""
    trend: str
    intensity: float  # 0-1 scale
    start_time: datetime
    duration: timedelta
    affected_content: List[str] = field(default_factory=list)  # Feed IDs
    momentum_boost: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "trend": self.trend,
            "intensity": self.intensity,
            "start_time": self.start_time.isoformat(),
            "duration_hours": self.duration.total_seconds() / 3600,
            "affected_content_count": len(self.affected_content),
            "momentum_boost": self.momentum_boost
        }


class TrendDecayModel:
    """趋势衰减模型 - Model trend lifecycle and decay"""

    def __init__(self, config: Optional[TrendConfig] = None):
        """
        Initialize trend decay model

        Args:
            config: Trend configuration
        """
        self.config = config or TrendConfig()
        self.active_trends: Dict[str, TrendLifecycle] = {}
        self.trend_history: Dict[str, TrendLifecycle] = {}

        logger.info("TrendDecayModel initialized", config=self.config.to_dict())

    @logger.trace_decorator
    def model_trend_lifecycle(
        self,
        trend: str,
        initial_momentum: float,
        start_time: Optional[datetime] = None
    ) -> TrendLifecycle:
        """
        建模趋势生命周期
        Model complete trend lifecycle

        Args:
            trend: Trend identifier (hashtag, topic, etc.)
            initial_momentum: Initial momentum value
            start_time: Trend start time (defaults to now)

        Returns:
            TrendLifecycle with all phases modeled
        """
        logger.info(f"Modeling lifecycle for trend '{trend}'", initial_momentum=initial_momentum)

        try:
            start_time = start_time or datetime.utcnow()

            phases = [
                self._model_emergence_phase(trend, initial_momentum, start_time),
                self._model_growth_phase(trend, initial_momentum, start_time),
                self._model_peak_phase(trend, initial_momentum, start_time),
                self._model_decline_phase(trend, initial_momentum, start_time),
                self._model_tail_phase(trend, initial_momentum, start_time)
            ]

            # Calculate peak momentum
            peak_momentum = max([max(p.momentum_curve) for p in phases if p.momentum_curve], default=0.0)

            lifecycle = TrendLifecycle(
                trend=trend,
                phases=phases,
                start_time=start_time,
                current_phase=TrendPhase.EMERGENCE,
                peak_momentum=peak_momentum
            )

            self.active_trends[trend] = lifecycle

            logger.info(
                f"Lifecycle modeled for trend '{trend}'",
                peak_momentum=peak_momentum,
                total_duration_hours=sum(p.duration_hours for p in phases)
            )

            return lifecycle

        except Exception as e:
            logger.error(f"Error modeling lifecycle for trend '{trend}'", exception=e)
            raise

    def _model_emergence_phase(
        self,
        trend: str,
        initial_momentum: float,
        start_time: datetime
    ) -> TrendPhaseData:
        """
        建模萌芽阶段
        Model emergence phase - slow initial growth
        """
        duration = self.config.emergence_duration_hours
        end_time = start_time + timedelta(hours=duration)

        # Slow exponential growth
        steps = 20
        momentum_curve = []
        for i in range(steps):
            progress = i / steps
            momentum = initial_momentum * (1 + progress * 0.5)  # 50% growth
            momentum_curve.append(momentum)

        return TrendPhaseData(
            phase=TrendPhase.EMERGENCE,
            start_time=start_time,
            end_time=end_time,
            duration_hours=duration,
            momentum_curve=momentum_curve,
            engagement_multiplier=1.1
        )

    def _model_growth_phase(
        self,
        trend: str,
        initial_momentum: float,
        start_time: datetime
    ) -> TrendPhaseData:
        """
        建模增长阶段
        Model growth phase - rapid exponential growth
        """
        emergence_duration = self.config.emergence_duration_hours
        phase_start = start_time + timedelta(hours=emergence_duration)

        duration = self.config.growth_duration_hours
        end_time = phase_start + timedelta(hours=duration)

        # Rapid exponential growth
        steps = 30
        momentum_curve = []
        base_momentum = initial_momentum * 1.5

        for i in range(steps):
            progress = i / steps
            # Exponential growth: momentum = base * e^(3*progress)
            momentum = base_momentum * math.exp(3 * progress)
            momentum_curve.append(momentum)

        return TrendPhaseData(
            phase=TrendPhase.GROWTH,
            start_time=phase_start,
            end_time=end_time,
            duration_hours=duration,
            momentum_curve=momentum_curve,
            engagement_multiplier=2.0
        )

    def _model_peak_phase(
        self,
        trend: str,
        initial_momentum: float,
        start_time: datetime
    ) -> TrendPhaseData:
        """
        建模峰值阶段
        Model peak phase - maximum momentum plateau
        """
        previous_duration = (
            self.config.emergence_duration_hours +
            self.config.growth_duration_hours
        )
        phase_start = start_time + timedelta(hours=previous_duration)

        duration = self.config.peak_duration_hours
        end_time = phase_start + timedelta(hours=duration)

        # Plateau at peak with small fluctuations
        steps = 20
        peak_momentum = initial_momentum * math.exp(3) * 1.5
        momentum_curve = []

        for i in range(steps):
            # Small random fluctuations around peak
            fluctuation = random.uniform(-0.1, 0.1)
            momentum = peak_momentum * (1 + fluctuation)
            momentum_curve.append(momentum)

        return TrendPhaseData(
            phase=TrendPhase.PEAK,
            start_time=phase_start,
            end_time=end_time,
            duration_hours=duration,
            momentum_curve=momentum_curve,
            engagement_multiplier=3.0
        )

    def _model_decline_phase(
        self,
        trend: str,
        initial_momentum: float,
        start_time: datetime
    ) -> TrendPhaseData:
        """
        建模衰减阶段
        Model decline phase - rapid decay from peak
        """
        previous_duration = (
            self.config.emergence_duration_hours +
            self.config.growth_duration_hours +
            self.config.peak_duration_hours
        )
        phase_start = start_time + timedelta(hours=previous_duration)

        duration = self.config.decline_duration_hours
        end_time = phase_start + timedelta(hours=duration)

        # Exponential decay
        steps = 30
        peak_momentum = initial_momentum * math.exp(3) * 1.5
        momentum_curve = []

        for i in range(steps):
            progress = i / steps
            # Exponential decay: momentum = peak * e^(-3*progress)
            momentum = peak_momentum * math.exp(-3 * progress)
            momentum_curve.append(momentum)

        return TrendPhaseData(
            phase=TrendPhase.DECLINE,
            start_time=phase_start,
            end_time=end_time,
            duration_hours=duration,
            momentum_curve=momentum_curve,
            engagement_multiplier=1.5
        )

    def _model_tail_phase(
        self,
        trend: str,
        initial_momentum: float,
        start_time: datetime
    ) -> TrendPhaseData:
        """
        建模尾部阶段
        Model tail phase - long slow decay to baseline
        """
        previous_duration = (
            self.config.emergence_duration_hours +
            self.config.growth_duration_hours +
            self.config.peak_duration_hours +
            self.config.decline_duration_hours
        )
        phase_start = start_time + timedelta(hours=previous_duration)

        duration = self.config.tail_duration_hours
        end_time = phase_start + timedelta(hours=duration)

        # Slow logarithmic decay to baseline
        steps = 50
        start_momentum = initial_momentum * math.exp(-3) * 1.5
        momentum_curve = []

        for i in range(steps):
            progress = i / steps
            # Logarithmic decay approaching baseline
            momentum = start_momentum * (1 - math.log10(1 + 9 * progress))
            momentum = max(momentum, initial_momentum * 0.5)  # Floor at 50% of initial
            momentum_curve.append(momentum)

        return TrendPhaseData(
            phase=TrendPhase.TAIL,
            start_time=phase_start,
            end_time=end_time,
            duration_hours=duration,
            momentum_curve=momentum_curve,
            engagement_multiplier=1.0
        )

    @logger.trace_decorator
    def apply_trend_shock(
        self,
        trend: str,
        shock_intensity: float,
        affected_feeds: List[Feed],
        duration: Optional[timedelta] = None
    ) -> TrendShock:
        """
        应用趋势冲击
        Apply sudden trend shock (breaking news, viral event, etc.)

        Args:
            trend: Trend identifier
            shock_intensity: Intensity of shock (0-1)
            affected_feeds: Feeds related to this trend
            duration: Duration of shock effect

        Returns:
            TrendShock object
        """
        logger.info(
            f"Applying trend shock for '{trend}'",
            intensity=shock_intensity,
            affected_feeds=len(affected_feeds)
        )

        try:
            duration = duration or timedelta(hours=6)
            start_time = datetime.utcnow()

            # Calculate momentum boost
            momentum_boost = shock_intensity * 1000  # High intensity = major boost

            # Boost virality of affected content
            boosted_feeds = []
            for feed in affected_feeds:
                if self._is_trend_relevant(feed, trend):
                    self._boost_content_virality(feed, shock_intensity)
                    boosted_feeds.append(feed.id)

            shock = TrendShock(
                trend=trend,
                intensity=shock_intensity,
                start_time=start_time,
                duration=duration,
                affected_content=boosted_feeds,
                momentum_boost=momentum_boost
            )

            # If trend already exists, inject momentum boost
            if trend in self.active_trends:
                lifecycle = self.active_trends[trend]
                # Boost current phase momentum
                current_time = datetime.utcnow()
                for phase_data in lifecycle.phases:
                    if phase_data.start_time <= current_time < phase_data.end_time:
                        phase_data.momentum_curve = [
                            m * (1 + shock_intensity) for m in phase_data.momentum_curve
                        ]
                        break

            logger.info(
                f"Trend shock applied for '{trend}'",
                boosted_feeds=len(boosted_feeds),
                momentum_boost=momentum_boost
            )

            return shock

        except Exception as e:
            logger.error(f"Error applying trend shock for '{trend}'", exception=e)
            return TrendShock(
                trend=trend,
                intensity=0.0,
                start_time=datetime.utcnow(),
                duration=timedelta(hours=1)
            )

    def _is_trend_relevant(self, feed: Feed, trend: str) -> bool:
        """
        检查Feed是否与趋势相关
        Check if feed is relevant to trend
        """
        # Check text content
        if trend.lower() in feed.text.lower():
            return True

        # Check hashtags
        if feed.entities and feed.entities.hashtags:
            hashtags = [tag.tag.lower() for tag in feed.entities.hashtags]
            if trend.lower() in hashtags:
                return True

        return False

    def _boost_content_virality(self, feed: Feed, intensity: float):
        """
        增强内容病毒性
        Boost content virality metrics
        """
        # Boost engagement metrics proportionally
        boost_factor = 1 + intensity

        feed.public_metrics.like_count = int(feed.public_metrics.like_count * boost_factor)
        feed.public_metrics.retweet_count = int(feed.public_metrics.retweet_count * boost_factor)
        feed.public_metrics.quote_count = int(feed.public_metrics.quote_count * boost_factor)
        feed.public_metrics.reply_count = int(feed.public_metrics.reply_count * boost_factor)

        if feed.public_metrics.impression_count:
            feed.public_metrics.impression_count = int(
                feed.public_metrics.impression_count * boost_factor
            )

        logger.debug(
            f"Boosted virality for feed {feed.id}",
            intensity=intensity,
            boost_factor=boost_factor
        )

    @logger.trace_decorator
    def calculate_trend_momentum(
        self,
        trend: str,
        time_window: timedelta = timedelta(hours=1),
        mention_count: Optional[int] = None,
        engagement_sum: Optional[int] = None
    ) -> float:
        """
        计算趋势动量
        Calculate current trend momentum

        Momentum = (Mentions * Avg_Engagement) / Time_Window

        Args:
            trend: Trend identifier
            time_window: Time window for calculation
            mention_count: Number of mentions (optional)
            engagement_sum: Sum of engagement (optional)

        Returns:
            Trend momentum value
        """
        logger.debug(f"Calculating momentum for trend '{trend}'")

        try:
            # If no data provided, use lifecycle model
            if trend in self.active_trends:
                lifecycle = self.active_trends[trend]
                momentum = lifecycle.get_current_momentum(datetime.utcnow())
                logger.info(f"Momentum for '{trend}': {momentum}")
                return momentum

            # Calculate from provided data
            if mention_count is not None and engagement_sum is not None:
                avg_engagement = engagement_sum / max(mention_count, 1)
                time_hours = time_window.total_seconds() / 3600

                momentum = (mention_count * avg_engagement) / time_hours

                logger.info(
                    f"Calculated momentum for '{trend}'",
                    momentum=momentum,
                    mentions=mention_count,
                    avg_engagement=avg_engagement
                )

                return momentum

            # Default low momentum if no data
            return 1.0

        except Exception as e:
            logger.error(f"Error calculating momentum for '{trend}'", exception=e)
            return 0.0

    def get_trend_phase(self, trend: str, current_time: Optional[datetime] = None) -> TrendPhase:
        """
        获取趋势当前阶段
        Get current phase of trend

        Args:
            trend: Trend identifier
            current_time: Current time (defaults to now)

        Returns:
            Current TrendPhase
        """
        current_time = current_time or datetime.utcnow()

        if trend not in self.active_trends:
            return TrendPhase.EMERGENCE

        lifecycle = self.active_trends[trend]

        for phase_data in lifecycle.phases:
            if phase_data.start_time <= current_time < phase_data.end_time:
                return phase_data.phase

        # Trend has ended
        return TrendPhase.TAIL

    def get_engagement_multiplier(
        self,
        trend: str,
        current_time: Optional[datetime] = None
    ) -> float:
        """
        获取趋势的互动倍增因子
        Get engagement multiplier for trend at current time

        Args:
            trend: Trend identifier
            current_time: Current time (defaults to now)

        Returns:
            Engagement multiplier (1.0 - 3.0)
        """
        current_time = current_time or datetime.utcnow()

        if trend not in self.active_trends:
            return 1.0

        lifecycle = self.active_trends[trend]

        for phase_data in lifecycle.phases:
            if phase_data.start_time <= current_time < phase_data.end_time:
                return phase_data.engagement_multiplier

        return 1.0

    def archive_trend(self, trend: str):
        """
        归档趋势
        Archive trend to history
        """
        if trend in self.active_trends:
            self.trend_history[trend] = self.active_trends[trend]
            del self.active_trends[trend]

            logger.info(f"Archived trend '{trend}'")
