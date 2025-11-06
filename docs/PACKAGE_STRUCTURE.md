# Feed Package Structure

## Overview

Feed is a focused data structure library for Twitter/X data modeling. This document describes the package organization.

## Directory Structure

```
Feed/
├── feed/                      # Main package
│   ├── __init__.py           # Package exports
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   ├── feed.py          # Core Feed entity
│   │   ├── entities.py      # Hashtags, mentions, URLs
│   │   ├── metrics.py       # Engagement metrics
│   │   ├── references.py    # Tweet references
│   │   └── user.py          # User model
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── manager.py       # FeedManager for CRUD
│       ├── entities.py      # Entity extraction
│       └── generators.py    # ID generation
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_feed.py
├── docs/                    # Documentation
│   ├── USAGE.md
│   └── PACKAGE_STRUCTURE.md (this file)
├── README.md               # Main documentation
├── QUICKSTART.md          # Quick start guide
├── setup.py               # Package configuration
├── requirements.txt       # Dependencies (none!)
├── .gitignore            # Git ignore patterns
└── LICENSE               # MIT License
```

## Package Organization

### `feed/` - Main Package

The root package that exports all public APIs.

**What it does:**
- Exports all models and utilities
- Provides clean import interface
- No business logic, just re-exports

**How to use:**
```python
import feed

# Access everything from top level
tweet = feed.Feed(...)
manager = feed.FeedManager()
entities = feed.extract_entities(text)
```

### `feed/models/` - Data Models

Pure data structures with no business logic.

**Files:**
- `feed.py` - Main Feed (tweet) entity
- `entities.py` - Hashtags, mentions, URLs
- `metrics.py` - Engagement metrics (likes, retweets, etc.)
- `references.py` - Tweet references (replies, quotes)
- `user.py` - User/author model

**Characteristics:**
- Dataclass-based
- Type-hinted
- Serializable (to_dict/from_dict)
- Twitter API v2 compatible

### `feed/utils/` - Utilities

Helper functions and management classes.

**Files:**
- `manager.py` - FeedManager for CRUD operations
- `entities.py` - Regex-based entity extraction
- `generators.py` - ID and sample data generation

**Characteristics:**
- Stateless utilities (except FeedManager)
- No dependencies on external libraries
- Helper functions for common operations

## Module Responsibilities

### `feed/models/feed.py`

**Purpose:** Core Feed (tweet) data structure

**Key classes:**
- `Feed` - Main tweet entity
- `FeedType` - Enum for tweet types

**No business logic:** Just data representation

**Example:**
```python
from feed.models import Feed, FeedType

tweet = Feed(
    id="123",
    text="Hello!",
    author_id="user_1",
    feed_type=FeedType.POST
)
```

### `feed/models/entities.py`

**Purpose:** Entity models for tweet content

**Key classes:**
- `HashtagEntity` - #hashtag
- `MentionEntity` - @mention
- `UrlEntity` - URLs
- `Entities` - Container for all entities

**Example:**
```python
from feed.models import Entities, HashtagEntity

entities = Entities(
    hashtags=[HashtagEntity(start=0, end=7, tag="Python")],
    mentions=[],
    urls=[]
)
```

### `feed/models/metrics.py`

**Purpose:** Engagement metrics

**Key classes:**
- `PublicMetrics` - Likes, retweets, replies, etc.

**Example:**
```python
from feed.models import PublicMetrics

metrics = PublicMetrics(
    like_count=100,
    retweet_count=25,
    reply_count=10
)
```

### `feed/models/references.py`

**Purpose:** Tweet references (replies, quotes, retweets)

**Key classes:**
- `ReferencedFeedType` - Enum for reference types
- `ReferencedFeed` - Reference to another tweet

**Example:**
```python
from feed.models import ReferencedFeed, ReferencedFeedType

ref = ReferencedFeed(
    type=ReferencedFeedType.REPLIED_TO.value,
    id="original_tweet_id"
)
```

### `feed/models/user.py`

**Purpose:** User/author model

**Key classes:**
- `User` - Twitter user information

**Example:**
```python
from feed.models import User

user = User(
    id="123",
    username="johndoe",
    name="John Doe",
    verified=False
)
```

### `feed/utils/manager.py`

**Purpose:** Tweet CRUD operations

**Key classes:**
- `FeedManager` - Create, save, load, search tweets

**Example:**
```python
from feed.utils import FeedManager

manager = FeedManager(storage_dir="./tweets")

# Create
tweet = manager.create_feed(text="...", author_id="...")

# Save
filepath = manager.save_feed(tweet)

# Load
loaded = manager.load_feed(filepath)

# Search
results = manager.search_feeds(text_contains="Python")
```

### `feed/utils/entities.py`

**Purpose:** Extract entities from text

**Key functions:**
- `extract_entities(text)` - Parse hashtags, mentions, URLs

**Example:**
```python
from feed.utils import extract_entities

text = "Hello @user #Python https://example.com"
entities = extract_entities(text)
```

### `feed/utils/generators.py`

**Purpose:** Generate IDs and sample data

**Key functions:**
- `generate_feed_id()` - Create unique tweet ID
- `create_sample_user()` - Generate test user

**Example:**
```python
from feed.utils import generate_feed_id, create_sample_user

tweet_id = generate_feed_id()
user = create_sample_user(user_id="123")
```

## Import Patterns

### Top-Level Imports (Recommended)

```python
import feed

# Models
tweet = feed.Feed(...)
feed_type = feed.FeedType.POST
metrics = feed.PublicMetrics(...)

# Utilities
manager = feed.FeedManager()
entities = feed.extract_entities(text)
```

### Detailed Imports

```python
from feed.models import Feed, FeedType, PublicMetrics
from feed.utils import FeedManager, extract_entities

tweet = Feed(...)
manager = FeedManager()
```

## Design Principles

### 1. Focused Scope
- **Data structures only**
- No simulation logic
- No analytics
- No API clients

### 2. Clean Separation
- **Models** = Pure data
- **Utils** = Helper functions
- No mixing of concerns

### 3. Zero Dependencies
- Python standard library only
- No version conflicts
- Easy to install

### 4. Type Safety
- Full type hints
- Dataclass-based
- IDE-friendly

### 5. Twitter API Compatible
- Matches Twitter API v2 structure
- Compatible JSON format
- Standard field names

## Testing

```bash
# Run tests
python tests/test_feed.py

# With pytest
pytest tests/
```

## Building On Top

Feed is designed as a foundation. Build your simulator separately:

```python
# Your simulator package
import feed

class TwitterSimulator:
    def __init__(self):
        self.manager = feed.FeedManager()
    
    def simulate(self):
        # Your simulation logic
        tweet = self.manager.create_feed(...)
        tweet.entities = feed.extract_entities(tweet.text)
        # Add your metrics, behaviors, etc.
        return tweet
```

## File Naming

**Tweets saved as:**
```
feed-{YYYYMMDD_HHMMSS}-{unique_id}.json
```

**Example:**
```
feed-20251106_120000-1762462374804.json
```

## JSON Format

Tweets stored as Twitter API v2 compatible JSON:

```json
{
  "id": "123456789",
  "text": "Hello World! #Python",
  "author_id": "user_1",
  "created_at": "2025-11-06T12:00:00.000Z",
  "feed_type": "post",
  "conversation_id": "123456789",
  "entities": {
    "hashtags": [{"start": 13, "end": 20, "tag": "Python"}],
    "mentions": [],
    "urls": []
  },
  "public_metrics": {
    "like_count": 0,
    "retweet_count": 0,
    "reply_count": 0,
    "quote_count": 0,
    "bookmark_count": 0
  },
  "lang": "en",
  "source": "Twitter Web App"
}
```

## Best Practices

1. **Use FeedManager** for consistent operations
2. **Extract entities** after setting text
3. **Type hints** help catch errors early
4. **Save tweets** in JSON format for portability
5. **Build simulation** in separate package

## Summary

Feed is a **focused data structure library** providing:
- ✅ Clean models for Twitter data
- ✅ Essential utilities
- ✅ Zero dependencies
- ✅ Type safety
- ✅ Twitter API v2 compatibility

**Not included (build separately):**
- ❌ Simulation logic
- ❌ Content generation
- ❌ User behavior modeling
- ❌ Analytics

---

*This keeps Feed clean, focused, and reusable across projects!*

