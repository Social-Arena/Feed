# Feed - Twitter Data Structure Library

A clean Python package for Twitter/X data modeling built entirely on top of Pydantic for concise, validated data structures.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
git clone https://github.com/Social-Arena/Feed
cd Feed
pip install -e .
```

## Quick Start

```python
import feed

# Create tweet
tweet = feed.Feed(
    id=feed.generate_feed_id(),
    text="Hello Twitter! #Python",
    author_id="user_123"
)

# Extract entities
tweet.entities = feed.extract_entities(tweet.text)

# Save/Load (one feed = one JSON)
feed.save_feed(tweet, "tweets/my_tweet.json")
loaded = feed.load_feed("tweets/my_tweet.json")
```

## Models

**Feed** - Main tweet structure  
**FeedType** - `POST`, `REPLY`, `QUOTE`, `RETWEET`, `THREAD`  
**Entities** - Hashtags, mentions, URLs  
**PublicMetrics** - Engagement counts  
**User** - User profile

## Usage

```python
# Create
tweet = feed.Feed(id=feed.generate_feed_id(), text="Hello!", author_id="user1")

# Entities
tweet.entities = feed.extract_entities(tweet.text)

# Metrics
tweet.public_metrics.like_count = 100

# Save/Load
feed.save_feed(tweet, "tweets/tweet.json")
loaded = feed.load_feed("tweets/tweet.json")
```

## Requirements

Python 3.8+ • [Pydantic](https://docs.pydantic.dev/) runtime validation

## License

MIT
