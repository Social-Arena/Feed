"""
Feed - Twitter Simulation Framework

A comprehensive Python package for Twitter data modeling and simulation.
"""

__version__ = "1.0.0"
__author__ = "Feed Module"

# Import core models
from .models import (
    Feed,
    FeedType,
    Entities,
    HashtagEntity,
    MentionEntity,
    UrlEntity,
    PublicMetrics,
    ReferencedFeed,
    ReferencedFeedType,
    User,
)

# Import utilities
from .utils import (
    FeedManager,
    extract_entities,
    generate_feed_id,
    create_sample_user,
)

# Import simulation components
from .simulation import (
    TwitterSimulator,
    SimulationConfig,
    UserBehavior,
    ContentGenerator,
    EngagementCalculator,
)

__all__ = [
    # Models
    "Feed",
    "FeedType",
    "Entities",
    "HashtagEntity",
    "MentionEntity",
    "UrlEntity",
    "PublicMetrics",
    "ReferencedFeed",
    "ReferencedFeedType",
    "User",
    
    # Utilities
    "FeedManager",
    "extract_entities",
    "generate_feed_id",
    "create_sample_user",
    
    # Simulation
    "TwitterSimulator",
    "SimulationConfig",
    "UserBehavior",
    "ContentGenerator",
    "EngagementCalculator",
]

# Convenience functions
def create_tweet(text: str, author_id: str, **kwargs) -> Feed:
    """
    Quick function to create a tweet without instantiating a manager.
    
    Args:
        text: Tweet content
        author_id: Author's ID
        **kwargs: Additional tweet parameters
        
    Returns:
        Feed object
    """
    manager = FeedManager()
    return manager.create_feed(text, author_id, **kwargs)


def simulate_twitter(num_tweets: int = 100, num_users: int = 50) -> tuple:
    """
    Quick function to run a Twitter simulation.
    
    Args:
        num_tweets: Number of tweets to generate
        num_users: Number of users to simulate
        
    Returns:
        Tuple of (tweets, statistics)
    """
    config = SimulationConfig(num_tweets=num_tweets, num_users=num_users)
    simulator = TwitterSimulator(config)
    return simulator.simulate()

