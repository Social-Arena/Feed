"""
Brand Safety - Ensure content is safe for brand associations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import re

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class BrandSafetyConfig:
    """品牌安全配置 - Brand safety configuration"""
    enable_keyword_filter: bool = True
    enable_context_analysis: bool = True
    enable_audience_matching: bool = True
    safety_threshold: float = 0.7

    def to_dict(self) -> Dict:
        return {
            "enable_keyword_filter": self.enable_keyword_filter,
            "enable_context_analysis": self.enable_context_analysis,
            "enable_audience_matching": self.enable_audience_matching,
            "safety_threshold": self.safety_threshold
        }


@dataclass
class BrandContext:
    """品牌上下文 - Brand context information"""
    brand_name: str
    brand_values: List[str] = field(default_factory=list)
    target_audience: Dict[str, any] = field(default_factory=dict)
    excluded_topics: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "brand_name": self.brand_name,
            "brand_values": self.brand_values,
            "target_audience": self.target_audience,
            "excluded_topics": self.excluded_topics
        }


@dataclass
class BrandSafetyAssessment:
    """品牌安全评估 - Brand safety assessment result"""
    content_id: str
    brand: str
    keyword_flags: List[str] = field(default_factory=list)
    context_alignment_score: float = 0.5
    audience_match_score: float = 0.5
    overall_brand_safety_score: float = 0.5
    is_brand_safe_result: bool = True
    issues: List[str] = field(default_factory=list)

    def is_brand_safe(self, threshold: float = 0.7) -> bool:
        """Check if content is brand safe"""
        return self.overall_brand_safety_score >= threshold

    def to_dict(self) -> Dict:
        return {
            "content_id": self.content_id,
            "brand": self.brand,
            "keyword_flags": self.keyword_flags,
            "context_alignment_score": self.context_alignment_score,
            "audience_match_score": self.audience_match_score,
            "overall_brand_safety_score": self.overall_brand_safety_score,
            "is_brand_safe": self.is_brand_safe(),
            "issues": self.issues
        }


class ContextAnalyzer:
    """上下文分析器 - Analyze content context for brand alignment"""

    def analyze_brand_alignment(
        self,
        feed: Feed,
        brand_context: BrandContext
    ) -> float:
        """
        分析品牌对齐度
        Analyze brand alignment score

        Args:
            feed: Feed to analyze
            brand_context: Brand context

        Returns:
            Alignment score (0-1)
        """
        score = 0.5  # Neutral baseline

        # Check brand values alignment
        if brand_context.brand_values:
            value_matches = 0
            for value in brand_context.brand_values:
                if value.lower() in feed.text.lower():
                    value_matches += 1

            if value_matches > 0:
                score += 0.2 * (value_matches / len(brand_context.brand_values))

        # Check for excluded topics
        if brand_context.excluded_topics:
            for topic in brand_context.excluded_topics:
                if topic.lower() in feed.text.lower():
                    score -= 0.3
                    break

        return max(0.0, min(score, 1.0))


class BrandSafety:
    """品牌安全 - Brand safety checker"""

    def __init__(self, config: Optional[BrandSafetyConfig] = None):
        """
        Initialize brand safety checker

        Args:
            config: Brand safety configuration
        """
        self.config = config or BrandSafetyConfig()
        self.unsafe_keywords = self._load_unsafe_keywords()
        self.context_analyzer = ContextAnalyzer()

        logger.info("BrandSafety initialized", config=self.config.to_dict())

    def _load_unsafe_keywords(self) -> Set[str]:
        """Load unsafe keywords for brand safety"""
        return {
            "violence", "hate", "discrimination", "offensive",
            "controversial", "scandal", "lawsuit", "illegal",
            "explicit", "adult", "nsfw"
        }

    @logger.trace_decorator
    def assess_brand_safety(
        self,
        feed: Feed,
        brand_context: BrandContext
    ) -> BrandSafetyAssessment:
        """
        评估品牌安全性
        Assess brand safety for content

        Args:
            feed: Feed to assess
            brand_context: Brand context information

        Returns:
            BrandSafetyAssessment result
        """
        logger.debug(
            f"Assessing brand safety for feed {feed.id}",
            brand=brand_context.brand_name
        )

        try:
            assessment = BrandSafetyAssessment(
                content_id=feed.id,
                brand=brand_context.brand_name
            )

            # Keyword checking
            if self.config.enable_keyword_filter:
                assessment.keyword_flags = self._check_unsafe_keywords(feed.text)

            # Context analysis
            if self.config.enable_context_analysis:
                assessment.context_alignment_score = self.context_analyzer.analyze_brand_alignment(
                    feed,
                    brand_context
                )

            # Audience matching
            if self.config.enable_audience_matching:
                assessment.audience_match_score = self._calculate_audience_match(
                    feed,
                    brand_context.target_audience
                )

            # Calculate overall score
            assessment.overall_brand_safety_score = self._calculate_overall_score(assessment)

            # Collect issues
            if assessment.keyword_flags:
                assessment.issues.append(
                    f"Unsafe keywords detected: {', '.join(assessment.keyword_flags[:3])}"
                )

            if assessment.context_alignment_score < 0.5:
                assessment.issues.append("Low brand alignment")

            if assessment.audience_match_score < 0.5:
                assessment.issues.append("Poor audience match")

            assessment.is_brand_safe_result = assessment.is_brand_safe(
                self.config.safety_threshold
            )

            logger.info(
                f"Brand safety assessed for {feed.id}",
                brand=brand_context.brand_name,
                score=assessment.overall_brand_safety_score,
                is_safe=assessment.is_brand_safe_result
            )

            return assessment

        except Exception as e:
            logger.error(
                f"Error assessing brand safety for {feed.id}",
                exception=e
            )
            raise

    def _check_unsafe_keywords(self, text: str) -> List[str]:
        """Check for unsafe keywords"""
        text_lower = text.lower()
        found_keywords = []

        for keyword in self.unsafe_keywords:
            if re.search(r'\b' + keyword + r'\b', text_lower):
                found_keywords.append(keyword)

        return found_keywords

    def _calculate_audience_match(
        self,
        feed: Feed,
        target_audience: Dict
    ) -> float:
        """Calculate audience match score"""
        # Simple heuristic based on language and content type
        score = 0.5

        # Check language match
        if target_audience.get('language') == feed.lang:
            score += 0.2

        # Check content appropriateness
        if not feed.possibly_sensitive:
            score += 0.2

        # Check engagement quality (proxy for audience interest)
        total_engagement = (
            feed.public_metrics.like_count +
            feed.public_metrics.retweet_count +
            feed.public_metrics.reply_count
        )

        if total_engagement > 100:
            score += 0.1

        return min(score, 1.0)

    def _calculate_overall_score(self, assessment: BrandSafetyAssessment) -> float:
        """Calculate overall brand safety score"""
        # Start with context and audience scores
        base_score = (
            assessment.context_alignment_score * 0.5 +
            assessment.audience_match_score * 0.5
        )

        # Penalize for unsafe keywords
        if assessment.keyword_flags:
            keyword_penalty = len(assessment.keyword_flags) * 0.1
            base_score -= keyword_penalty

        return max(0.0, min(base_score, 1.0))

    @logger.trace_decorator
    def create_brand_safe_feed_collection(
        self,
        feeds: List[Feed],
        brand: BrandContext
    ) -> List[Feed]:
        """
        创建品牌安全的Feed集合
        Create brand-safe feed collection

        Args:
            feeds: List of feeds
            brand: Brand context

        Returns:
            List of brand-safe feeds
        """
        logger.info(
            f"Creating brand-safe collection for {brand.brand_name}",
            total_feeds=len(feeds)
        )

        try:
            safe_feeds = []

            for feed in feeds:
                assessment = self.assess_brand_safety(feed, brand)
                if assessment.is_brand_safe(self.config.safety_threshold):
                    safe_feeds.append(feed)

            logger.info(
                f"Created brand-safe collection",
                brand=brand.brand_name,
                safe_count=len(safe_feeds),
                total_count=len(feeds)
            )

            return safe_feeds

        except Exception as e:
            logger.error(
                f"Error creating brand-safe collection for {brand.brand_name}",
                exception=e
            )
            return []
