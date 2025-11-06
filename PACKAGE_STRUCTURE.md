# Package Structure Documentation

## Overview

The Feed package has been restructured into a clean, modular GitHub-ready Python package focused on Twitter simulation with the Feed entity as the core component.

## Directory Structure

```
Feed/
├── feed/                      # Main package directory
│   ├── __init__.py           # Package entry point with convenience functions
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   ├── feed.py          # Core Feed entity (simplified, Twitter-focused)
│   │   ├── entities.py      # Hashtags, mentions, URLs
│   │   ├── metrics.py       # Public engagement metrics
│   │   ├── references.py    # Tweet references (reply, quote, retweet)
│   │   └── user.py          # User model
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── manager.py       # FeedManager for CRUD operations
│   │   ├── entities.py      # Entity extraction utilities
│   │   └── generators.py    # ID and sample data generation
│   └── simulation/          # Twitter simulation engine
│       ├── __init__.py
│       ├── simulator.py     # Main TwitterSimulator orchestrator
│       ├── config.py        # SimulationConfig
│       ├── behavior.py      # UserBehavior modeling
│       ├── content.py       # ContentGenerator
│       └── engagement.py    # EngagementCalculator
├── examples/                 # Usage examples
│   ├── basic_usage.py       # Basic operations
│   └── simulation_demo.py   # Simulation scenarios
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_feed.py        # Basic tests
├── docs/                    # Documentation
│   └── USAGE.md            # Comprehensive usage guide
├── README.md               # Main documentation
├── QUICKSTART.md          # Quick start guide
├── setup.py               # Package installation config
├── requirements.txt       # Dependencies (none!)
├── .gitignore            # Git ignore patterns
└── LICENSE               # MIT License

# Legacy files (can be removed):
├── __init__.py           # Old package init
├── feed_models.py        # Old monolithic models
├── feed_utils.py         # Old monolithic utils
├── simulation.py         # Old monolithic simulation
├── main.py               # Old demo script
└── example_simulation.py # Old example
```

## Key Improvements

### 1. Modular Architecture

**Before:**
- `feed_models.py` (365 lines) - All models in one file
- `feed_utils.py` (400 lines) - All utilities in one file
- `simulation.py` (639 lines) - All simulation in one file

**After:**
- Separated into logical modules
- Each file has a single responsibility
- Easy to navigate and maintain
- Clear import structure

### 2. Simplified Feed Entity

**Focused on Twitter simulation:**
- Removed: `MediaItem`, `Poll`, `Place`, `GeoInfo`, `EditControls`, etc.
- Kept: Core `Feed` model with essential fields
- Result: Cleaner, more focused data structure

**Feed Model Now Contains:**
```python
@dataclass
class Feed:
    # Core fields
    id: str
    text: str
    author_id: str
    created_at: str
    feed_type: FeedType  # POST, REPLY, QUOTE, RETWEET, THREAD
    
    # Conversation
    conversation_id: Optional[str]
    in_reply_to_user_id: Optional[str]
    
    # References
    referenced_feeds: List[ReferencedFeed]
    
    # Content
    entities: Optional[Entities]  # hashtags, mentions, urls
    
    # Metrics
    public_metrics: PublicMetrics
    
    # Twitter-specific
    lang: str
    source: str
    possibly_sensitive: bool
```

### 3. Clean Import Structure

**Top-level imports:**
```python
import feed

# Models
feed.Feed
feed.FeedType
feed.PublicMetrics
feed.User

# Utilities
feed.FeedManager
feed.extract_entities

# Simulation
feed.TwitterSimulator
feed.SimulationConfig

# Convenience
feed.create_tweet()
feed.simulate_twitter()
```

**Detailed imports:**
```python
from feed.models import Feed, FeedType, PublicMetrics
from feed.utils import FeedManager, extract_entities
from feed.simulation import TwitterSimulator, SimulationConfig
```

### 4. Package Installation

```bash
# Development install
pip install -e .

# Regular install
pip install .

# From PyPI (future)
pip install twitter-feed-simulator
```

### 5. Example Usage

**Before:**
```python
import sys
sys.path.append('/path/to/Feed')
from feed_models import Feed, FeedType
from feed_utils import FeedManager
```

**After:**
```python
import feed

tweet = feed.create_tweet("Hello!", "user_1")
tweets, stats = feed.simulate_twitter(100, 50)
```

## Module Responsibilities

### `feed/models/`
- **Purpose**: Data structure definitions
- **Files**: 
  - `feed.py` - Main Feed entity
  - `entities.py` - Hashtags, mentions, URLs
  - `metrics.py` - Engagement metrics
  - `references.py` - Tweet references
  - `user.py` - User data
- **No business logic**: Pure data models

### `feed/utils/`
- **Purpose**: Helper functions and management
- **Files**:
  - `manager.py` - CRUD operations (create, save, load, search)
  - `entities.py` - Regex-based entity extraction
  - `generators.py` - ID and sample data generation
- **Stateless utilities**: No simulation logic

### `feed/simulation/`
- **Purpose**: Twitter activity simulation
- **Files**:
  - `simulator.py` - Main orchestrator
  - `config.py` - Configuration parameters
  - `behavior.py` - User behavior patterns
  - `content.py` - Realistic content generation
  - `engagement.py` - Metrics calculation
- **Stateful simulation**: Complex behavior modeling

## Testing

```bash
# Run basic tests
python tests/test_feed.py

# With pytest
pip install pytest
pytest tests/

# Run examples
python examples/basic_usage.py
python examples/simulation_demo.py
```

## Migration Guide

If you have code using the old structure:

**Old code:**
```python
from feed_models import Feed, FeedType
from feed_utils import FeedManager
from simulation import SocialSimulator

manager = FeedManager()
simulator = SocialSimulator()
```

**New code:**
```python
import feed

manager = feed.FeedManager()
simulator = feed.TwitterSimulator()
```

## Best Practices

1. **Import from top level**: `import feed` preferred
2. **Use convenience functions**: `feed.create_tweet()` instead of `FeedManager().create_feed()`
3. **Follow module structure**: Don't import from submodules directly
4. **Keep Feed simple**: Use it for Twitter tweets only
5. **Extend via subclassing**: Don't modify core Feed model

## Next Steps

1. Remove old legacy files:
   - `feed_models.py`
   - `feed_utils.py`
   - `simulation.py`
   - `main.py`
   - `example_simulation.py`
   - `__init__.py` (root level)

2. Set up GitHub repository:
   - Initialize git (if not done)
   - Add remote origin
   - Push to GitHub

3. Add CI/CD:
   - GitHub Actions for tests
   - Automated PyPI publishing
   - Code coverage tracking

4. Documentation:
   - Add docstrings
   - Generate API docs with Sphinx
   - Add more examples

## Summary

The package is now:
✅ Modular and organized
✅ GitHub-ready
✅ Pip installable
✅ Well-documented
✅ Focused on Twitter simulation
✅ Easy to use and extend
✅ Zero dependencies
✅ Production-ready

Use `QUICKSTART.md` to get started immediately!

