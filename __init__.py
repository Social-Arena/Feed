"""
Feed Module - Social Media Feed Data Structure and Simulation

A comprehensive, platform-agnostic feed data structure for social media simulation
and data management. Compatible with Twitter/X API v2 while supporting multiple platforms.

Example:
    import feed
    
    # Create a feed manager
    manager = feed.FeedManager()
    
    # Create a simple feed
    my_feed = manager.create_feed(
        text="Hello World! #FirstPost",
        author_id="user123",
        platform="twitter"
    )
    
    # Run a social simulation
    simulator = feed.SocialSimulator()
    simulator.simulate_activity(num_feeds=100, duration_hours=24)
"""

__version__ = "1.0.0"
__author__ = "Feed Module"
__all__ = [
    # Core Models
    "Feed",
    "FeedType",
    "FeedResponse",
    "User",
    "MediaItem",
    "Poll",
    "PollOption",
    "Place",
    "GeoInfo",
    "Entities",
    "HashtagEntity",
    "MentionEntity", 
    "UrlEntity",
    "PublicMetrics",
    "ReferencedFeed",
    "ReferencedFeedType",
    "ContextAnnotation",
    "EditControls",
    "Attachments",
    
    # Utilities
    "FeedManager",
    "extract_entities",
    "create_sample_user",
    "create_sample_media",
    "create_thread",
    
    # Simulation
    "SocialSimulator",
    "SimulationConfig",
    "UserBehavior",
    "ContentGenerator",
    "EngagementSimulator",
    
    # Convenience Functions
    "create_feed",
    "load_feed",
    "save_feed",
    "generate_feeds",
]

# Import core models
from .feed_models import (
    Feed,
    FeedType,
    FeedResponse,
    User,
    MediaItem,
    Poll,
    PollOption,
    Place,
    GeoInfo,
    Entities,
    HashtagEntity,
    MentionEntity,
    UrlEntity,
    PublicMetrics,
    ReferencedFeed,
    ReferencedFeedType,
    ContextAnnotation,
    EditControls,
    Attachments,
)

# Import utilities
from .feed_utils import (
    FeedManager,
    extract_entities,
    create_sample_user,
    create_sample_media,
    create_thread,
)

# Import simulation components (to be created)
from .simulation import (
    SocialSimulator,
    SimulationConfig,
    UserBehavior,
    ContentGenerator,
    EngagementSimulator,
)

# Convenience functions for quick usage
def create_feed(text: str, author_id: str, **kwargs) -> Feed:
    """
    Quick function to create a feed without instantiating a manager.
    
    Args:
        text: Feed content
        author_id: Author's ID
        **kwargs: Additional feed parameters
        
    Returns:
        Feed object
    """
    manager = FeedManager()
    return manager.create_feed(text, author_id, **kwargs)


def load_feed(filepath: str) -> Feed:
    """
    Quick function to load a feed from file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Feed object
    """
    manager = FeedManager()
    return manager.load_feed(filepath)


def save_feed(feed: Feed, storage_dir: str = "./feeds") -> str:
    """
    Quick function to save a feed to file.
    
    Args:
        feed: Feed object to save
        storage_dir: Directory to save in
        
    Returns:
        Path to saved file
    """
    manager = FeedManager(storage_dir)
    return manager.save_feed(feed)


def generate_feeds(count: int = 10, platform: str = "generic") -> list:
    """
    Generate sample feeds for testing.
    
    Args:
        count: Number of feeds to generate
        platform: Platform to simulate
        
    Returns:
        List of Feed objects
    """
    simulator = SocialSimulator()
    return simulator.generate_sample_feeds(count, platform)
