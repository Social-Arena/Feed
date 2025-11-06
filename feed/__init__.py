"""
Feed - Twitter Data Structure Library

A clean, focused Python package for Twitter/X data modeling.
This is a pure data structure library - build your simulation on top of it!
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
]
