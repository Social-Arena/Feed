"""
Configuration for Twitter simulation
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class SimulationConfig:
    """Configuration for Twitter simulation"""
    num_users: int = 100
    num_tweets: int = 1000
    duration_hours: int = 24
    
    # Activity patterns
    peak_hours: List[int] = field(default_factory=lambda: [9, 12, 18, 21])
    min_tweets_per_user: int = 1
    max_tweets_per_user: int = 10
    
    # Engagement rates (as percentages)
    like_rate: float = 0.15  # 15% chance of liking
    retweet_rate: float = 0.03  # 3% chance of retweeting
    reply_rate: float = 0.05  # 5% chance of replying
    quote_rate: float = 0.02  # 2% chance of quoting
    
    # Content distribution
    reply_probability: float = 0.20  # 20% of tweets are replies
    quote_probability: float = 0.10  # 10% of tweets are quotes
    retweet_probability: float = 0.05  # 5% of tweets are retweets

