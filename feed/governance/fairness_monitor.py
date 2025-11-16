"""
Fairness Monitor - Monitor algorithmic fairness and bias
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class FairnessMetrics:
    """公平性指标 - Fairness metrics for a group"""
    group_name: str
    total_impressions: int = 0
    avg_engagement_rate: float = 0.0
    avg_content_quality: float = 0.0
    representation_ratio: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "group_name": self.group_name,
            "total_impressions": self.total_impressions,
            "avg_engagement_rate": self.avg_engagement_rate,
            "avg_content_quality": self.avg_content_quality,
            "representation_ratio": self.representation_ratio
        }


@dataclass
class FairnessReport:
    """公平性报告 - Complete fairness report"""
    group_metrics: Dict[str, FairnessMetrics] = field(default_factory=dict)
    disparity_metrics: Dict[str, float] = field(default_factory=dict)
    overall_fairness_score: float = 1.0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "group_metrics": {k: v.to_dict() for k, v in self.group_metrics.items()},
            "disparity_metrics": self.disparity_metrics,
            "overall_fairness_score": self.overall_fairness_score,
            "recommendations": self.recommendations
        }


@dataclass
class BiasDetection:
    """偏见检测 - Bias detection result"""
    bias_type: str
    severity: float  # 0-1
    affected_groups: List[str]
    is_significant: bool
    description: str

    def to_dict(self) -> Dict:
        return {
            "bias_type": self.bias_type,
            "severity": self.severity,
            "affected_groups": self.affected_groups,
            "is_significant": self.is_significant,
            "description": self.description
        }


class FairnessMonitor:
    """公平性监控器 - Monitor algorithmic fairness"""

    def __init__(self):
        """Initialize fairness monitor"""
        logger.info("FairnessMonitor initialized")

    @logger.trace_decorator
    def monitor_demographic_fairness(
        self,
        recommendations: List[Dict],
        user_demographics: Optional[Dict] = None
    ) -> FairnessReport:
        """
        监控人口统计学公平性
        Monitor demographic fairness in recommendations

        Args:
            recommendations: List of recommendations with metadata
            user_demographics: Optional demographic information

        Returns:
            FairnessReport with analysis
        """
        logger.info(f"Monitoring fairness for {len(recommendations)} recommendations")

        try:
            report = FairnessReport()

            # Group by demographics if available
            if user_demographics:
                demographic_groups = self._group_by_demographics(
                    recommendations,
                    user_demographics
                )
            else:
                # Default grouping by content type
                demographic_groups = self._group_by_content_type(recommendations)

            # Calculate metrics for each group
            for group_name, group_recs in demographic_groups.items():
                metrics = self._calculate_group_metrics(group_recs)
                report.group_metrics[group_name] = metrics

            # Calculate disparity metrics
            report.disparity_metrics = self._calculate_disparity_metrics(
                report.group_metrics
            )

            # Calculate overall fairness score
            report.overall_fairness_score = self._calculate_overall_fairness(
                report.disparity_metrics
            )

            # Generate recommendations
            if report.overall_fairness_score < 0.7:
                report.recommendations = self._generate_fairness_recommendations(report)

            logger.info(
                f"Fairness monitoring completed",
                overall_score=report.overall_fairness_score,
                groups=len(report.group_metrics)
            )

            return report

        except Exception as e:
            logger.error("Error monitoring fairness", exception=e)
            return FairnessReport()

    def _group_by_demographics(
        self,
        recommendations: List[Dict],
        demographics: Dict
    ) -> Dict[str, List[Dict]]:
        """Group recommendations by demographics"""
        groups = defaultdict(list)

        for rec in recommendations:
            # Simple grouping by age group (example)
            user_id = rec.get('user_id')
            if user_id in demographics:
                age_group = demographics[user_id].get('age_group', 'unknown')
                groups[age_group].append(rec)
            else:
                groups['unknown'].append(rec)

        return dict(groups)

    def _group_by_content_type(self, recommendations: List[Dict]) -> Dict[str, List[Dict]]:
        """Group by content type"""
        groups = defaultdict(list)

        for rec in recommendations:
            content_type = rec.get('content_type', 'general')
            groups[content_type].append(rec)

        return dict(groups)

    def _calculate_group_metrics(self, group_recs: List[Dict]) -> FairnessMetrics:
        """Calculate metrics for a group"""
        if not group_recs:
            return FairnessMetrics(group_name="empty")

        total_impressions = sum(r.get('impressions', 0) for r in group_recs)
        avg_engagement = sum(r.get('engagement_rate', 0.0) for r in group_recs) / len(group_recs)
        avg_quality = sum(r.get('quality_score', 0.5) for r in group_recs) / len(group_recs)

        return FairnessMetrics(
            group_name=group_recs[0].get('group_name', 'group'),
            total_impressions=total_impressions,
            avg_engagement_rate=avg_engagement,
            avg_content_quality=avg_quality,
            representation_ratio=len(group_recs) / 100  # Normalized
        )

    def _calculate_disparity_metrics(
        self,
        group_metrics: Dict[str, FairnessMetrics]
    ) -> Dict[str, float]:
        """Calculate disparity between groups"""
        if len(group_metrics) < 2:
            return {"disparity": 0.0}

        # Calculate engagement rate disparity
        engagement_rates = [m.avg_engagement_rate for m in group_metrics.values()]
        max_engagement = max(engagement_rates)
        min_engagement = min(engagement_rates)

        engagement_disparity = (max_engagement - min_engagement) / max(max_engagement, 0.01)

        # Calculate representation disparity
        representations = [m.representation_ratio for m in group_metrics.values()]
        max_repr = max(representations)
        min_repr = min(representations)

        repr_disparity = (max_repr - min_repr) / max(max_repr, 0.01)

        return {
            "engagement_disparity": engagement_disparity,
            "representation_disparity": repr_disparity,
            "overall_disparity": (engagement_disparity + repr_disparity) / 2
        }

    def _calculate_overall_fairness(self, disparity_metrics: Dict[str, float]) -> float:
        """Calculate overall fairness score (1.0 = perfectly fair)"""
        overall_disparity = disparity_metrics.get('overall_disparity', 0.0)
        fairness = 1.0 - overall_disparity
        return max(0.0, min(fairness, 1.0))

    def _generate_fairness_recommendations(self, report: FairnessReport) -> List[str]:
        """Generate recommendations for improving fairness"""
        recommendations = []

        if report.disparity_metrics.get('engagement_disparity', 0.0) > 0.3:
            recommendations.append("Consider boosting engagement opportunities for underperforming groups")

        if report.disparity_metrics.get('representation_disparity', 0.0) > 0.3:
            recommendations.append("Balance content representation across demographic groups")

        return recommendations

    @logger.trace_decorator
    def detect_bias_in_recommendations(
        self,
        recommendations: List[Dict]
    ) -> List[BiasDetection]:
        """
        检测推荐中的偏见
        Detect bias in recommendations

        Args:
            recommendations: List of recommendations

        Returns:
            List of bias detections
        """
        logger.info(f"Detecting bias in {len(recommendations)} recommendations")

        try:
            bias_detections = []

            # Detect diversity bias
            diversity_bias = self._detect_diversity_bias(recommendations)
            if diversity_bias.is_significant:
                bias_detections.append(diversity_bias)

            # Detect author fairness bias
            author_bias = self._detect_author_fairness_bias(recommendations)
            if author_bias.is_significant:
                bias_detections.append(author_bias)

            logger.info(f"Detected {len(bias_detections)} significant biases")

            return bias_detections

        except Exception as e:
            logger.error("Error detecting bias", exception=e)
            return []

    def _detect_diversity_bias(self, recommendations: List[Dict]) -> BiasDetection:
        """Detect lack of content diversity"""
        # Simple diversity check: unique authors vs total recommendations
        unique_authors = len(set(r.get('author_id') for r in recommendations))
        total_recs = len(recommendations)

        diversity_ratio = unique_authors / total_recs if total_recs > 0 else 0.0

        severity = 1.0 - diversity_ratio
        is_significant = severity > 0.5

        return BiasDetection(
            bias_type="diversity",
            severity=severity,
            affected_groups=["all_users"],
            is_significant=is_significant,
            description=f"Low content diversity: {diversity_ratio:.2%} unique authors"
        )

    def _detect_author_fairness_bias(self, recommendations: List[Dict]) -> BiasDetection:
        """Detect unfair author representation"""
        # Check if small number of authors dominate recommendations
        author_counts = defaultdict(int)
        for rec in recommendations:
            author_counts[rec.get('author_id', 'unknown')] += 1

        if not author_counts:
            return BiasDetection(
                bias_type="author_fairness",
                severity=0.0,
                affected_groups=[],
                is_significant=False,
                description="No data"
            )

        # Calculate concentration (Gini-like metric)
        counts = sorted(author_counts.values(), reverse=True)
        top_10_percent = max(1, len(counts) // 10)
        top_concentration = sum(counts[:top_10_percent]) / sum(counts)

        severity = top_concentration if top_concentration > 0.5 else 0.0
        is_significant = severity > 0.7

        return BiasDetection(
            bias_type="author_fairness",
            severity=severity,
            affected_groups=["minority_authors"],
            is_significant=is_significant,
            description=f"Top 10% authors represent {top_concentration:.1%} of recommendations"
        )
