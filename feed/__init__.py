"""
Feed - Twitter Data Structure Library & Viral Simulation System

A comprehensive Python package for Twitter/X data modeling and viral propagation simulation.
Includes data structures, viral metrics, engagement simulation, governance, and analytics.
"""

__version__ = "2.0.0"
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

# Import feed extensions
from .feed_extensions import (
    ViralFeed,
    SponsoredFeed,
)

# Import simulation API
from .api import (
    FeedSimulationAPI,
    GovernanceFilterConfig,
)

# Import simulation manager
from .utils.simulation_manager import (
    SimulationFeedManager,
    SimulationConfig,
)

__all__ = [
    # Core Models
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

    # Core Utilities
    "FeedManager",
    "extract_entities",
    "generate_feed_id",
    "create_sample_user",

    # Feed Extensions
    "ViralFeed",
    "SponsoredFeed",

    # Simulation API
    "FeedSimulationAPI",
    "GovernanceFilterConfig",
    "SimulationFeedManager",
    "SimulationConfig",
]

# Submodules available for import
# from feed.simulation import ViralityCalculator, EngagementSimulator, TrendDecayModel, SessionManager
# from feed.governance import SafetyFilter, FairnessMonitor, BrandSafety
# from feed.analytics import ViralityAnalyzer, InfluenceTracker
