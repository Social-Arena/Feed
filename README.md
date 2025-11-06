# Feed - Twitter Data Structure Library

A clean, focused Python package for Twitter/X data modeling. This library provides the core data structures - **build your simulation on top of it!**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is Feed?

Feed is a **pure data structure library** that provides:
- 🐦 **Twitter/X data models** following the official API v2 structure
- 📊 **Clean, Pythonic interfaces** using dataclasses
- 🔧 **Essential utilities** for managing tweet data
- 🚀 **Zero dependencies** - pure Python standard library

**What Feed is NOT:**
- ❌ Not a simulation framework (build that separately!)
- ❌ Not a Twitter API client
- ❌ Not an analytics platform

## Why Use Feed?

✅ **Foundation for your Twitter projects** - Clean data structures you can build on  
✅ **Twitter API v2 compatible** - Matches official structure  
✅ **Type-safe** - Full type hints throughout  
✅ **Battle-tested** - Comprehensive test suite  
✅ **Zero dependencies** - No version conflicts  
✅ **Well-documented** - Clear examples and API docs  

## Installation

### From Source

```bash
git clone https://github.com/yourusername/feed.git
cd Feed
pip install -e .
```

### As a Dependency

```bash
pip install twitter-feed-structure
```

Or in your `requirements.txt`:
```
twitter-feed-structure>=1.0.0
```

## Quick Start

### 1. Create a Tweet

```python
import feed

manager = feed.FeedManager()

tweet = manager.create_feed(
    text="Hello Twitter! #Python #DataStructures",
    author_id="user_123"
)

print(f"Tweet ID: {tweet.id}")
print(f"Text: {tweet.text}")
```

### 2. Extract Entities

```python
import feed

text = "Check out @elonmusk's post about #AI https://example.com"
entities = feed.extract_entities(text)

print(f"Hashtags: {[h.tag for h in entities.hashtags]}")
print(f"Mentions: {[m.username for m in entities.mentions]}")
print(f"URLs: {[u.expanded_url for u in entities.urls]}")
```

### 3. Create a Reply Thread

```python
import feed

manager = feed.FeedManager()

# Original tweet
original = manager.create_feed(
    text="What's everyone working on?",
    author_id="user_1"
)

# Reply to it
reply = manager.create_feed(
    text="@user_1 Building a Twitter data structure library!",
    author_id="user_2",
    feed_type=feed.FeedType.REPLY,
    conversation_id=original.id,
    in_reply_to_user_id="user_1",
    referenced_feeds=[
        feed.ReferencedFeed(
            type=feed.ReferencedFeedType.REPLIED_TO.value,
            id=original.id
        )
    ]
)
```

### 4. Save and Load Tweets

```python
import feed

manager = feed.FeedManager(storage_dir="./tweets")

# Save
tweet = manager.create_feed(text="Save me!", author_id="user_1")
filepath = manager.save_feed(tweet)

# Load
loaded = manager.load_feed(filepath)

# Load all
all_tweets = manager.load_all_feeds()
```

### 5. Set Engagement Metrics

```python
import feed

tweet = manager.create_feed(
    text="Popular tweet!",
    author_id="user_1"
)

tweet.public_metrics = feed.PublicMetrics(
    like_count=150,
    retweet_count=45,
    reply_count=23,
    quote_count=8,
    bookmark_count=12,
    impression_count=5000
)
```

## Package Structure

```
feed/
├── models/              # Core data models
│   ├── feed.py         # Main Feed entity
│   ├── entities.py     # Hashtags, mentions, URLs
│   ├── metrics.py      # Engagement metrics
│   ├── references.py   # Tweet references
│   └── user.py         # User model
└── utils/              # Utilities
    ├── manager.py      # FeedManager for CRUD
    ├── entities.py     # Entity extraction
    └── generators.py   # ID generation
```

## Core Data Models

### Feed

The main tweet data structure:

```python
@dataclass
class Feed:
    id: str                                    # Unique tweet ID
    text: str                                  # Tweet content
    author_id: str                             # Author's user ID
    created_at: str                            # ISO 8601 timestamp
    feed_type: FeedType                        # POST, REPLY, QUOTE, etc.
    conversation_id: Optional[str]             # Thread ID
    in_reply_to_user_id: Optional[str]        # Parent tweet author
    referenced_feeds: List[ReferencedFeed]     # Replies, quotes, retweets
    entities: Optional[Entities]               # Hashtags, mentions, URLs
    public_metrics: PublicMetrics              # Engagement stats
    lang: str                                  # Language code
    source: str                                # Client used
    possibly_sensitive: bool                   # Content flag
```

### FeedType

```python
class FeedType(Enum):
    POST = "post"           # Standard tweet
    REPLY = "reply"         # Reply to another tweet
    QUOTE = "quote"         # Quote tweet
    RETWEET = "retweet"     # Retweet
    THREAD = "thread"       # Thread continuation
```

### PublicMetrics

```python
@dataclass
class PublicMetrics:
    like_count: int
    retweet_count: int
    reply_count: int
    quote_count: int
    bookmark_count: int
    impression_count: Optional[int]
```

### Entities

```python
@dataclass
class Entities:
    hashtags: List[HashtagEntity]    # #tag
    mentions: List[MentionEntity]    # @user
    urls: List[UrlEntity]            # https://...
```

### User

```python
@dataclass
class User:
    id: str
    username: str
    name: str
    verified: bool
    description: Optional[str]
    public_metrics: Optional[Dict[str, int]]
```

## FeedManager API

```python
manager = feed.FeedManager(storage_dir="./tweets")

# Create
tweet = manager.create_feed(text, author_id, **kwargs)

# Save
filepath = manager.save_feed(tweet)

# Load
tweet = manager.load_feed(filepath)
all_tweets = manager.load_all_feeds()

# Search
results = manager.search_feeds(
    text_contains="Python",
    author_id="user_123",
    feed_type=feed.FeedType.POST
)
```

## JSON Format

Tweets are stored in Twitter API v2 compatible JSON:

```json
{
  "id": "1234567890",
  "text": "Hello Twitter! #Python",
  "author_id": "user_123",
  "created_at": "2025-11-06T12:00:00.000Z",
  "feed_type": "post",
  "conversation_id": "1234567890",
  "entities": {
    "hashtags": [
      {"start": 15, "end": 22, "tag": "Python"}
    ],
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

## Use Cases

### 🎯 Build Your Simulator
Use Feed as the foundation for your Twitter simulation engine:
```python
import feed

# Your simulator uses Feed structures
class TwitterSimulator:
    def __init__(self):
        self.manager = feed.FeedManager()
    
    def generate_tweet(self):
        return self.manager.create_feed(...)
```

### 📊 Analytics & Research
Store and analyze Twitter data:
```python
import feed

manager = feed.FeedManager()
tweets = manager.load_all_feeds()

# Analyze
total_likes = sum(t.public_metrics.like_count for t in tweets)
avg_engagement = total_likes / len(tweets)
```

### 🧪 Testing
Generate test data for your Twitter apps:
```python
import feed

# Create test fixtures
def create_test_tweet():
    return feed.FeedManager().create_feed(
        text="Test tweet",
        author_id="test_user"
    )
```

### 🔄 Data Migration
Convert between formats:
```python
import feed

# Load from your format
tweet = feed.Feed.from_dict(your_data)

# Save in Twitter API format
manager.save_feed(tweet)
```

## Testing

```bash
# Run tests
python tests/test_feed.py

# With pytest
pip install pytest
pytest tests/
```

## API Reference

### Top-Level Exports

```python
import feed

# Models
feed.Feed              # Main tweet structure
feed.FeedType          # Tweet types enum
feed.PublicMetrics     # Engagement metrics
feed.Entities          # Hashtags, mentions, URLs
feed.User              # User model
feed.ReferencedFeed    # Tweet references
feed.ReferencedFeedType # Reference types

# Utilities
feed.FeedManager       # CRUD operations
feed.extract_entities  # Parse text for entities
feed.generate_feed_id  # Generate unique IDs
feed.create_sample_user # Create test users
```

## Building a Simulator?

Feed provides the data structures. Here's how to build a simulator on top:

```python
import feed
import random

class MyTwitterSimulator:
    def __init__(self):
        self.manager = feed.FeedManager()
        self.tweets = []
    
    def create_random_tweet(self, author_id):
        """Generate a tweet with Feed structures"""
        tweet = self.manager.create_feed(
            text=self.generate_content(),
            author_id=author_id
        )
        
        # Add entities
        tweet.entities = feed.extract_entities(tweet.text)
        
        # Set metrics (your simulation logic here)
        tweet.public_metrics = feed.PublicMetrics(
            like_count=random.randint(0, 1000),
            retweet_count=random.randint(0, 100),
            reply_count=random.randint(0, 50)
        )
        
        return tweet
    
    def generate_content(self):
        """Your content generation logic"""
        return "Your simulated tweet content here #Python"
```

## Requirements

- Python 3.8 or higher
- No external dependencies!

## Contributing

Contributions welcome! This is a data structure library, so please keep it focused on:
- ✅ Core data models
- ✅ Essential utilities
- ✅ Type safety improvements
- ✅ Documentation
- ❌ Avoid adding simulation logic (that's for separate packages!)

## License

MIT License - see LICENSE file for details.

## Documentation

- `docs/USAGE.md` - Comprehensive usage guide
- `tests/test_feed.py` - Usage examples in tests

## Related Projects

Building something on top of Feed? Let us know!

---

**Built for the Twitter developer community** 🐦

*Need a simulator? Build it on top of Feed!*
