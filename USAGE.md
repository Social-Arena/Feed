# Feed Data Structure - Usage Guide

## Overview

The Feed data structure is a comprehensive, platform-agnostic implementation that mirrors the Twitter/X v2 API data model while supporting features from various social media platforms including TikTok, Instagram, and more.

## Installation

No external dependencies are required. The implementation uses only Python standard library modules (Python 3.8+).

```bash
# No installation needed, just run:
python3 main.py
```

## Quick Start

### Running the Demo

```bash
python3 main.py
```

This will:
- Generate 11 example feed items with various features
- Save them as JSON files with the naming pattern: `feed-{timestamp}-{unique_id}.json`
- Create a feed response file containing multiple feeds with expanded includes
- Demonstrate loading and searching capabilities

### Basic Usage

```python
from feed_models import Feed, FeedType
from feed_utils import FeedManager

# Initialize the manager
manager = FeedManager(storage_dir="./feeds")

# Create a simple feed
feed = manager.create_feed(
    text="Hello, world! #FirstPost",
    author_id="123456",
    feed_type=FeedType.POST,
    platform="twitter"
)

# Save the feed
filepath = manager.save_feed(feed)
print(f"Saved to: {filepath}")
```

## File Naming Convention

All feed files follow the pattern: `feed-{time}-{unique_identifier}.json`

- `time`: Timestamp in format YYYYMMDD_HHMMSS
- `unique_identifier`: Unique numeric identifier derived from feed ID

Example: `feed-20251105_235626-1762404986933206598.json`

## Feed Types Supported

- **POST**: Standard text post (Tweet-like)
- **VIDEO**: Video content (TikTok-like)
- **IMAGE_POST**: Image-focused post (Instagram-like)
- **STORY**: Ephemeral content
- **REEL**: Short video (Instagram Reels)
- **THREAD**: Connected series of posts

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
- **Entities**: Hashtags, mentions, URLs automatically extracted
- **Media**: Photos, videos, GIFs with metadata
- **Polls**: Multi-option polls with voting data
- **Location**: Geographic information and place data

### Metrics
- Engagement counts (likes, reposts, replies, quotes)
- View counts for videos
- Impressions and bookmarks

### Platform-Specific Features
- TikTok: Music ID, effects, duet/stitch settings
- Instagram: Story features, reel metadata
- Twitter: Edit history, reply settings

## Working with Feeds

### Creating Feeds

```python
# Create with entities extracted
feed = manager.create_feed(
    text="Check out @username's post! #Amazing https://example.com",
    author_id="123456",
    feed_type=FeedType.POST,
    platform="twitter"
)
feed.entities = extract_entities(feed.text)
```

### Loading Feeds

```python
# Load single feed
feed = manager.load_feed("feeds/feed-20251105_235626-123456.json")

# Load all feeds
all_feeds = manager.load_all_feeds()
```

### Searching Feeds

```python
# Search by text content
results = manager.search_feeds(text_contains="challenge")

# Filter by platform
twitter_feeds = manager.search_feeds(platform="twitter")

# Filter by type
video_feeds = manager.search_feeds(feed_type=FeedType.VIDEO)
```

### Creating Threads

```python
thread = create_thread(
    texts=[
        "1/ Starting a thread about Feed structures",
        "2/3 The structure is platform-agnostic",
        "3/3 Supporting multiple social platforms!"
    ],
    author_id="123456",
    manager=manager,
    platform="twitter"
)
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
    "repost_count": 5,
    ...
  }
}
```

### Feed Response (API-style)
```json
{
  "data": [...],  // Array of feeds
  "includes": {
    "users": [...],
    "media": [...],
    "places": [...],
    "polls": [...]
  },
  "meta": {
    "result_count": 5,
    "next_token": "..."
  }
}
```

## Advanced Features

### Edit History
Tracks post edits with `edit_history_feed_ids` and `edit_controls`

### Context Annotations
Semantic categorization for better understanding:
```python
feed.context_annotations = [
    ContextAnnotation(
        domain={"id": "46", "name": "Technology"},
        entity={"id": "1", "name": "Machine Learning"}
    )
]
```

### Content Moderation
- `possibly_sensitive`: Flag for sensitive content
- `withheld`: Content restriction information
- `reply_settings`: Control who can reply

## Files in This Project

- `feed_models.py`: Core data models and structures
- `feed_utils.py`: Utility functions and FeedManager class  
- `main.py`: Demo script with examples
- `requirements.txt`: Dependencies (none required)
- `feeds/`: Directory containing generated JSON files

## API Compatibility

The structure is designed to be compatible with Twitter/X API v2, making it easy to:
- Import real Twitter data
- Export to Twitter-compatible format
- Integrate with existing Twitter tools

## Extending the Structure

Add platform-specific features using the `platform_specific_data` field:

```python
feed.platform_specific_data = {
    "instagram_specific_field": "value",
    "custom_metadata": {...}
}
```

## Best Practices

1. Always extract entities after setting feed text
2. Use appropriate feed types for content
3. Set platform identifier for proper context
4. Include metrics for realistic data
5. Use conversation_id for threading
6. Save feeds immediately after creation

## Example Use Cases

- Social media analytics
- Content aggregation
- Cross-platform posting
- Data migration between platforms
- Social media simulation/testing
- Academic research on social media data
