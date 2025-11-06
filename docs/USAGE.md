# Feed Data Structure - Usage Guide

## Overview

Feed is a focused, Twitter/X-style data structure library implemented with Python dataclasses. It models tweets, entities, public metrics, references, and a simple manager for creating/saving/loading/searching feeds. No external dependencies are required (Python 3.8+).

## Installation

```bash
# From source
pip install -e .
```

## Quick Start

### Basic Usage

```python
import feed

# Initialize the manager
manager = feed.FeedManager(storage_dir="./feeds")

# Create a simple feed
tweet = manager.create_feed(
    text="Hello, world! #FirstPost",
    author_id="123456",
    feed_type=feed.FeedType.POST,
    platform="twitter"
)

# Save the feed
filepath = manager.save_feed(tweet)
print(f"Saved to: {filepath}")
```

## File Naming Convention

All feed files follow the pattern: `feed-{time}-{unique_identifier}.json`

- `time`: Timestamp in format YYYYMMDD_HHMMSS
- `unique_identifier`: Unique numeric identifier derived from feed ID

Example: `feed-20251105_235626-1762404986933206598.json`

## Feed Types Supported

- **POST**: Standard text post (Tweet-like)
- **REPLY**: Reply to another tweet
- **QUOTE**: Quote tweet
- **RETWEET**: Retweet
- **THREAD**: Thread continuation

## Key Features

### Core Fields
- `id`: Unique identifier
- `text`: Feed content
- `author_id`: Creator's ID
- `created_at`: ISO 8601 timestamp
- `feed_type`: Type of feed content
- `platform`: Source platform

### Relationships
- **Replies**: Link to parent posts via `in_reply_to_user_id` and `conversation_id`
- **Quotes**: Reference other feeds via `referenced_feeds`
- **Reposts**: Share content with or without comment
- **Threads**: Connected series of posts

### Rich Content
- **Entities**: Hashtags, mentions, URLs (regex-based extraction utility)

### Metrics
- Engagement counts (likes, reposts, replies, quotes)
- View counts for videos
- Impressions and bookmarks

### Platform-Specific Features
- This package focuses on Twitter-style fields. Other platforms are not modeled.

## Working with Feeds

### Creating Feeds

```python
# Create with entities extracted
tweet = manager.create_feed(
    text="Check out @username's post! #Amazing https://example.com",
    author_id="123456",
    feed_type=feed.FeedType.POST,
    platform="twitter"
)
tweet.entities = feed.extract_entities(tweet.text)
```

### Loading Feeds

```python
# Load single feed
tweet = manager.load_feed("feeds/feed-20251105_235626-123456.json")

# Load all feeds
all_feeds = manager.load_all_feeds()
```

### Searching Feeds

```python
# Search by text content
results = manager.search_feeds(text_contains="challenge")

# Filter by author
users_feeds = manager.search_feeds(author_id="123456")

# Filter by type
post_feeds = manager.search_feeds(feed_type=feed.FeedType.POST)
```

### Creating Threads

```python
def create_thread(texts, author_id, manager):
    thread = []
    conversation_id = None
    for i, text in enumerate(texts):
        if i == 0:
            tw = manager.create_feed(text=text, author_id=author_id)
            conversation_id = tw.id
        else:
            tw = manager.create_feed(
                text=text,
                author_id=author_id,
                feed_type=feed.FeedType.THREAD,
                conversation_id=conversation_id,
                in_reply_to_user_id=author_id,
                referenced_feeds=[
                    feed.ReferencedFeed(
                        type=feed.ReferencedFeedType.REPLIED_TO.value,
                        id=thread[-1].id
                    )
                ]
            )
        tw.entities = feed.extract_entities(text)
        thread.append(tw)
    return thread
```

## JSON Structure

### Single Feed
```json
{
  "id": "1762404986933206598",
  "text": "Hello, world! #FirstPost",
  "feed_type": "post",
  "author_id": "123456",
  "created_at": "2025-11-05T23:56:26.933198Z",
  "entities": {
    "hashtags": [...],
    "mentions": [...],
    "urls": [...]
  },
  "public_metrics": {
    "like_count": 15,
    "retweet_count": 5,
    ...
  }
}
```

### Multiple Feeds
```json
[
  { "id": "...", "text": "...", "feed_type": "post", ... },
  { "id": "...", "text": "...", "feed_type": "reply", ... }
]
```

## Notes
- `possibly_sensitive` flag is available.
- Public metrics fields include: `retweet_count`, `reply_count`, `like_count`, `quote_count`, `bookmark_count`, and optional `impression_count`.

## Files in This Project

- `feed/`: Package with models and utilities
- `requirements.txt`: Dependencies (none required)
- `feeds/`: Directory containing generated JSON files

## API Compatibility

The structure follows Twitter/X API v2 field names for core tweet-like data, making it easy to:
- Import real Twitter-like data
- Export to a compatible JSON format

## Extending the Structure

Keep platform-specific extensions in downstream projects to preserve this package’s focused scope.

## Best Practices

1. Always extract entities after setting feed text
2. Use appropriate feed types for content
3. Set platform identifier for proper context
4. Include metrics as needed
5. Use conversation_id for threading
6. Save feeds immediately after creation

## Example Use Cases

- Social media analytics
- Content aggregation
- Cross-platform posting
- Data migration between platforms
- Social media simulation/testing
- Academic research on social media data
