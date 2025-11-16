"""
Safety Filter - Content safety detection and filtering
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class SafetyConfig:
    """安全配置 - Safety filter configuration"""
    toxicity_threshold: float = 0.7
    misinformation_threshold: float = 0.8
    harmful_content_threshold: float = 0.9

    def to_dict(self) -> Dict:
        return {
            "toxicity_threshold": self.toxicity_threshold,
            "misinformation_threshold": self.misinformation_threshold,
            "harmful_content_threshold": self.harmful_content_threshold
        }


@dataclass
class SafetyAssessment:
    """安全评估 - Safety assessment result"""
    content_id: str
    toxicity_score: float = 0.0
    misinformation_score: float = 0.0
    harmful_content_indicators: List[str] = field(default_factory=list)
    overall_safety_score: float = 1.0
    issues: List[str] = field(default_factory=list)

    def is_safe(self, threshold: float = 0.7) -> bool:
        """Check if content is safe"""
        return self.overall_safety_score >= threshold

    def to_dict(self) -> Dict:
        return {
            "content_id": self.content_id,
            "toxicity_score": self.toxicity_score,
            "misinformation_score": self.misinformation_score,
            "harmful_content_indicators": self.harmful_content_indicators,
            "overall_safety_score": self.overall_safety_score,
            "issues": self.issues,
            "is_safe": self.is_safe()
        }


class ToxicityDetector:
    """毒性检测器 - Detect toxic content"""

    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        self.toxic_patterns = [
            r'\b(hate|racist|sexist|violent|threaten|kill|attack)\b',
            r'\b(stupid|idiot|moron|dumb|loser)\b',
            r'\b(fuck|shit|damn|hell)\b'
        ]

    def detect(self, text: str) -> float:
        """Detect toxicity score (0-1)"""
        text_lower = text.lower()
        matches = 0

        for pattern in self.toxic_patterns:
            if re.search(pattern, text_lower):
                matches += 1

        # Simple heuristic: normalize by number of patterns
        score = min(matches / len(self.toxic_patterns), 1.0)

        return score


class MisinformationDetector:
    """错误信息检测器 - Detect misinformation"""

    def __init__(self):
        self.suspicious_patterns = [
            r'\b(fake news|hoax|conspiracy|cover-up)\b',
            r'\b(they don\'t want you to know|hidden truth|secret)\b',
            r'\b(miracle cure|guaranteed|100% effective)\b'
        ]

    def detect(self, feed: Feed) -> float:
        """Detect misinformation score (0-1)"""
        text_lower = feed.text.lower()
        matches = 0

        for pattern in self.suspicious_patterns:
            if re.search(pattern, text_lower):
                matches += 1

        score = min(matches / len(self.suspicious_patterns), 1.0)

        return score


class HarmfulContentDetector:
    """有害内容检测器 - Detect harmful content"""

    def __init__(self):
        self.harmful_patterns = [
            r'\b(suicide|self-harm|hurt yourself)\b',
            r'\b(drug dealing|illegal drugs|buy drugs)\b',
            r'\b(child abuse|exploitation)\b'
        ]

    def detect(self, feed: Feed) -> List[str]:
        """Detect harmful content indicators"""
        text_lower = feed.text.lower()
        indicators = []

        for pattern in self.harmful_patterns:
            if re.search(pattern, text_lower):
                indicators.append(pattern)

        return indicators


class SafetyFilter:
    """安全过滤器 - Content safety filter"""

    def __init__(self, config: Optional[SafetyConfig] = None):
        """
        Initialize safety filter

        Args:
            config: Safety configuration
        """
        self.config = config or SafetyConfig()
        self.toxicity_detector = ToxicityDetector(self.config.toxicity_threshold)
        self.misinformation_detector = MisinformationDetector()
        self.harmful_content_detector = HarmfulContentDetector()

        logger.info("SafetyFilter initialized", config=self.config.to_dict())

    @logger.trace_decorator
    def assess_content_safety(self, feed: Feed) -> SafetyAssessment:
        """
        评估内容安全性
        Assess content safety

        Args:
            feed: Feed to assess

        Returns:
            SafetyAssessment result
        """
        logger.debug(f"Assessing safety for feed {feed.id}")

        try:
            assessment = SafetyAssessment(content_id=feed.id)

            # Toxicity detection
            assessment.toxicity_score = self.toxicity_detector.detect(feed.text)

            # Misinformation detection
            assessment.misinformation_score = self.misinformation_detector.detect(feed)

            # Harmful content detection
            assessment.harmful_content_indicators = self.harmful_content_detector.detect(feed)

            # Calculate overall safety score
            assessment.overall_safety_score = self._calculate_overall_safety(assessment)

            # Collect issues
            if assessment.toxicity_score > self.config.toxicity_threshold:
                assessment.issues.append("High toxicity detected")

            if assessment.misinformation_score > self.config.misinformation_threshold:
                assessment.issues.append("Potential misinformation detected")

            if assessment.harmful_content_indicators:
                assessment.issues.append(f"Harmful content indicators: {len(assessment.harmful_content_indicators)}")

            logger.info(
                f"Safety assessed for {feed.id}",
                overall_score=assessment.overall_safety_score,
                issues_count=len(assessment.issues)
            )

            return assessment

        except Exception as e:
            logger.error(f"Error assessing safety for {feed.id}", exception=e)
            raise

    def _calculate_overall_safety(self, assessment: SafetyAssessment) -> float:
        """Calculate overall safety score"""
        # Invert scores (high toxicity = low safety)
        toxicity_safety = 1.0 - assessment.toxicity_score
        misinformation_safety = 1.0 - assessment.misinformation_score
        harmful_safety = 1.0 if not assessment.harmful_content_indicators else 0.0

        # Weighted average
        overall = (
            toxicity_safety * 0.4 +
            misinformation_safety * 0.3 +
            harmful_safety * 0.3
        )

        return overall

    @logger.trace_decorator
    def filter_unsafe_content(
        self,
        feeds: List[Feed],
        safety_threshold: float = 0.7
    ) -> List[Feed]:
        """
        过滤不安全内容
        Filter out unsafe content

        Args:
            feeds: List of feeds to filter
            safety_threshold: Safety score threshold

        Returns:
            List of safe feeds
        """
        logger.info(f"Filtering {len(feeds)} feeds with threshold {safety_threshold}")

        try:
            safe_feeds = []

            for feed in feeds:
                assessment = self.assess_content_safety(feed)
                if assessment.overall_safety_score >= safety_threshold:
                    safe_feeds.append(feed)

            logger.info(
                f"Filtered to {len(safe_feeds)} safe feeds from {len(feeds)} total"
            )

            return safe_feeds

        except Exception as e:
            logger.error("Error filtering unsafe content", exception=e)
            return feeds

    def batch_assess(self, feeds: List[Feed]) -> List[SafetyAssessment]:
        """
        批量评估
        Batch assess multiple feeds

        Args:
            feeds: List of feeds

        Returns:
            List of safety assessments
        """
        assessments = []
        for feed in feeds:
            assessment = self.assess_content_safety(feed)
            assessments.append(assessment)

        return assessments
