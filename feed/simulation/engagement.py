"""
Engagement calculation for Twitter simulation
"""

import random
import math
from datetime import timedelta

from ..models import Feed, PublicMetrics
from .behavior import UserBehavior
from .config import SimulationConfig


class EngagementCalculator:
    """Calculate engagement metrics for tweets"""
    
    @staticmethod
    def calculate_engagement_score(
        feed: Feed,
        author_behavior: UserBehavior,
        time_since_tweet: timedelta
    ) -> float:
        """
        Calculate engagement score based on various factors.
        Returns a score between 0 and 1.
        """
        score = 0.5  # Base score
        
        # Author influence factor
        if author_behavior.activity_level == "influencer":
            score += 0.3
        elif author_behavior.activity_level == "high":
            score += 0.15
        elif author_behavior.activity_level == "medium":
            score += 0.05
        
        # Time decay factor (engagement decreases over time)
        hours_passed = time_since_tweet.total_seconds() / 3600
        time_factor = math.exp(-hours_passed / 24)  # Exponential decay over 24 hours
        score *= time_factor
        
        # Hashtag factor
        if feed.entities and feed.entities.hashtags:
            score += min(0.1, len(feed.entities.hashtags) * 0.03)
        
        return min(1.0, max(0.0, score))
    
    @staticmethod
    def generate_metrics(
        engagement_score: float,
        follower_count: int,
        config: SimulationConfig
    ) -> PublicMetrics:
        """Generate realistic metrics based on engagement score"""
        # Base reach (percentage of followers who see the tweet)
        reach = int(follower_count * engagement_score * random.uniform(0.1, 0.5))
        
        # Calculate metrics based on reach and config rates
        metrics = PublicMetrics(
            like_count=int(reach * config.like_rate * random.uniform(0.5, 1.5)),
            retweet_count=int(reach * config.retweet_rate * random.uniform(0.5, 1.5)),
            reply_count=int(reach * config.reply_rate * random.uniform(0.5, 1.5)),
            quote_count=int(reach * config.quote_rate * random.uniform(0.5, 1.5)),
            bookmark_count=int(reach * 0.01 * random.uniform(0.5, 1.5)),  # 1% bookmark rate
            impression_count=reach * random.randint(2, 5),  # Multiple views per user
        )
        
        return metrics
    
    @staticmethod
    def simulate_viral_growth(
        initial_metrics: PublicMetrics,
        hours_elapsed: int,
        virality_factor: float = 0.1
    ) -> PublicMetrics:
        """Simulate viral growth pattern over time"""
        if random.random() > virality_factor:
            return initial_metrics  # Not going viral
        
        # Viral growth formula
        growth_factor = 1 + math.log(hours_elapsed + 1) * virality_factor * 10
        
        return PublicMetrics(
            like_count=int(initial_metrics.like_count * growth_factor),
            retweet_count=int(initial_metrics.retweet_count * growth_factor * 1.5),  # Retweets drive virality
            reply_count=int(initial_metrics.reply_count * growth_factor * 0.8),
            quote_count=int(initial_metrics.quote_count * growth_factor * 1.2),
            bookmark_count=int(initial_metrics.bookmark_count * growth_factor * 0.6),
            impression_count=int(initial_metrics.impression_count * growth_factor * 2) if initial_metrics.impression_count else None,
        )

