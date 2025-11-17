"""
Virality Analyzer - Deep analysis of viral content patterns
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import Counter
import re

from ..models.feed import Feed
from ..utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)


@dataclass
class ViralContentPatterns:
    """病毒内容模式 - Patterns found in viral content"""
    content_patterns: Dict[str, int] = field(default_factory=dict)
    timing_patterns: Dict[str, float] = field(default_factory=dict)
    propagation_patterns: Dict[str, int] = field(default_factory=dict)
    common_hashtags: List[tuple] = field(default_factory=list)
    common_keywords: List[tuple] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "content_patterns": self.content_patterns,
            "timing_patterns": self.timing_patterns,
            "propagation_patterns": self.propagation_patterns,
            "common_hashtags": self.common_hashtags,
            "common_keywords": self.common_keywords
        }


@dataclass
class ViralityFactors:
    """病毒性因素 - Factors contributing to virality"""
    emotional_triggers: List[str] = field(default_factory=list)
    social_proof_elements: List[str] = field(default_factory=list)
    novelty_score: float = 0.0
    author_influence: float = 0.0
    network_position: str = "peripheral"
    timing_score: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "emotional_triggers": self.emotional_triggers,
            "social_proof_elements": self.social_proof_elements,
            "novelty_score": self.novelty_score,
            "author_influence": self.author_influence,
            "network_position": self.network_position,
            "timing_score": self.timing_score
        }


class ViralityAnalyzer:
    """病毒性分析器 - Analyze viral content characteristics"""

    def __init__(self):
        """Initialize virality analyzer"""
        self.emotional_keywords = {
            "positive": ["amazing", "incredible", "love", "wonderful", "awesome"],
            "negative": ["terrible", "awful", "hate", "disaster", "worst"],
            "surprise": ["shocking", "unbelievable", "unexpected", "wow"],
            "urgency": ["breaking", "urgent", "now", "alert", "important"]
        }

        logger.info("ViralityAnalyzer initialized")

    @logger.trace_decorator
    def analyze_viral_content_patterns(
        self,
        viral_feeds: List[Feed]
    ) -> ViralContentPatterns:
        """
        分析病毒内容模式
        Analyze patterns in viral content

        Args:
            viral_feeds: List of viral feeds

        Returns:
            ViralContentPatterns object
        """
        logger.info(f"Analyzing patterns in {len(viral_feeds)} viral feeds")

        try:
            patterns = ViralContentPatterns()

            # Extract content features
            patterns.content_patterns = self._extract_viral_content_features(viral_feeds)

            # Analyze timing patterns
            patterns.timing_patterns = self._analyze_viral_timing_patterns(viral_feeds)

            # Analyze propagation patterns
            patterns.propagation_patterns = self._analyze_propagation_paths(viral_feeds)

            # Find common hashtags
            all_hashtags = []
            for feed in viral_feeds:
                if feed.entities and feed.entities.hashtags:
                    all_hashtags.extend([tag.tag for tag in feed.entities.hashtags])

            hashtag_counts = Counter(all_hashtags)
            patterns.common_hashtags = hashtag_counts.most_common(10)

            # Find common keywords
            all_words = []
            for feed in viral_feeds:
                words = re.findall(r'\b\w+\b', feed.text.lower())
                all_words.extend([w for w in words if len(w) > 4])

            word_counts = Counter(all_words)
            patterns.common_keywords = word_counts.most_common(20)

            logger.info(
                "Pattern analysis completed",
                hashtag_count=len(patterns.common_hashtags),
                keyword_count=len(patterns.common_keywords)
            )

            return patterns

        except Exception as e:
            logger.error("Error analyzing viral patterns", exception=e)
            return ViralContentPatterns()

    def _extract_viral_content_features(self, viral_feeds: List[Feed]) -> Dict[str, int]:
        """Extract content features from viral feeds"""
        features = {
            "avg_text_length": 0,
            "with_hashtags": 0,
            "with_urls": 0,
            "with_mentions": 0,
            "with_media": 0
        }

        total_length = 0

        for feed in viral_feeds:
            total_length += len(feed.text)

            if feed.entities:
                if feed.entities.hashtags:
                    features["with_hashtags"] += 1
                if feed.entities.urls:
                    features["with_urls"] += 1
                if feed.entities.mentions:
                    features["with_mentions"] += 1

        if viral_feeds:
            features["avg_text_length"] = total_length // len(viral_feeds)

        return features

    def _analyze_viral_timing_patterns(self, viral_feeds: List[Feed]) -> Dict[str, float]:
        """Analyze timing patterns"""
        from datetime import datetime

        hour_counts = Counter()

        for feed in viral_feeds:
            try:
                created = datetime.fromisoformat(feed.created_at.rstrip('Z'))
                hour_counts[created.hour] += 1
            except:
                continue

        if not hour_counts:
            return {}

        total = sum(hour_counts.values())
        peak_hour = hour_counts.most_common(1)[0][0]

        return {
            "peak_hour": float(peak_hour),
            "peak_hour_percentage": hour_counts[peak_hour] / total if total > 0 else 0.0
        }

    def _analyze_propagation_paths(self, viral_feeds: List[Feed]) -> Dict[str, int]:
        """Analyze propagation patterns"""
        patterns = {
            "quote_tweets": 0,
            "retweets": 0,
            "replies": 0
        }

        for feed in viral_feeds:
            patterns["quote_tweets"] += feed.public_metrics.quote_count
            patterns["retweets"] += feed.public_metrics.retweet_count
            patterns["replies"] += feed.public_metrics.reply_count

        return patterns

    @logger.trace_decorator
    def identify_virality_factors(self, feed: Feed) -> ViralityFactors:
        """
        识别病毒传播因素
        Identify factors contributing to virality

        Args:
            feed: Feed to analyze

        Returns:
            ViralityFactors object
        """
        logger.debug(f"Identifying virality factors for {feed.id}")

        try:
            factors = ViralityFactors()

            # Identify emotional triggers
            factors.emotional_triggers = self._identify_emotional_triggers(feed.text)

            # Identify social proof elements
            factors.social_proof_elements = self._identify_social_proof(feed)

            # Calculate novelty score
            factors.novelty_score = self._calculate_novelty_score(feed)

            # Calculate author influence (simplified)
            factors.author_influence = self._calculate_author_influence(feed.author_id)

            # Analyze network position
            factors.network_position = self._analyze_network_position(feed.author_id)

            # Calculate timing score
            factors.timing_score = self._calculate_timing_score(feed)

            logger.info(
                f"Virality factors identified for {feed.id}",
                emotional_triggers=len(factors.emotional_triggers),
                novelty_score=factors.novelty_score
            )

            return factors

        except Exception as e:
            logger.error(f"Error identifying virality factors for {feed.id}", exception=e)
            return ViralityFactors()

    def _identify_emotional_triggers(self, text: str) -> List[str]:
        """Identify emotional triggers in text"""
        text_lower = text.lower()
        triggers = []

        for emotion, keywords in self.emotional_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    triggers.append(f"{emotion}:{keyword}")

        return triggers

    def _identify_social_proof(self, feed: Feed) -> List[str]:
        """Identify social proof elements"""
        proof_elements = []

        # High engagement is social proof
        if feed.public_metrics.like_count > 1000:
            proof_elements.append("high_likes")

        if feed.public_metrics.retweet_count > 500:
            proof_elements.append("high_shares")

        # Mentions of verified/influential accounts
        if feed.entities and feed.entities.mentions:
            proof_elements.append("mentions_others")

        return proof_elements

    def _calculate_novelty_score(self, feed: Feed) -> float:
        """Calculate content novelty score"""
        # Simple heuristic: unique word ratio
        words = feed.text.split()
        unique_words = set(words)

        if not words:
            return 0.0

        novelty = len(unique_words) / len(words)
        return min(novelty, 1.0)

    def _calculate_author_influence(self, author_id: str) -> float:
        """Calculate author influence (placeholder)"""
        # In real implementation, would look up author metrics
        return 0.5  # Default moderate influence

    def _analyze_network_position(self, author_id: str) -> str:
        """Analyze author's network position (placeholder)"""
        # In real implementation, would analyze network graph
        return "central"  # Default position

    def _calculate_timing_score(self, feed: Feed) -> float:
        """Calculate timing score"""
        from datetime import datetime

        try:
            created = datetime.fromisoformat(feed.created_at.rstrip('Z'))
            hour = created.hour

            # Peak hours: 9-11 AM, 1-3 PM, 7-9 PM
            if hour in [9, 10, 11, 13, 14, 15, 19, 20, 21]:
                return 1.0
            elif hour in [8, 12, 16, 17, 18, 22]:
                return 0.7
            else:
                return 0.4

        except:
            return 0.5
