"""
User behavior modeling for Twitter simulation
"""

import random
from dataclasses import dataclass, field
from typing import List


@dataclass
class UserBehavior:
    """Model for simulating Twitter user behavior patterns"""
    user_id: str
    username: str
    activity_level: str  # "low", "medium", "high", "influencer"
    interests: List[str]
    posting_frequency: float  # Tweets per hour
    engagement_probability: float
    follower_count: int
    following_count: int
    
    # Behavior patterns
    peak_activity_hours: List[int] = field(default_factory=list)
    hashtag_usage_rate: float = 0.3
    mention_rate: float = 0.2
    url_share_rate: float = 0.1
    
    def __post_init__(self):
        """Initialize behavior patterns based on activity level"""
        if self.activity_level == "low":
            self.posting_frequency = random.uniform(0.1, 0.3)
            self.engagement_probability = 0.1
            self.peak_activity_hours = random.sample(range(24), 2)
        elif self.activity_level == "medium":
            self.posting_frequency = random.uniform(0.3, 0.8)
            self.engagement_probability = 0.3
            self.peak_activity_hours = random.sample(range(24), 4)
        elif self.activity_level == "high":
            self.posting_frequency = random.uniform(0.8, 2.0)
            self.engagement_probability = 0.5
            self.peak_activity_hours = random.sample(range(24), 6)
        elif self.activity_level == "influencer":
            self.posting_frequency = random.uniform(2.0, 5.0)
            self.engagement_probability = 0.7
            self.peak_activity_hours = list(range(8, 23))  # Active most of the day

