# Feed - Social Media Data Structure & Simulation Module

A comprehensive Python module for social media feed data structures and simulation. This module provides a platform-agnostic implementation that mirrors the Twitter/X API v2 structure while supporting features from various social platforms including TikTok, Instagram, and more.

## Features

- 🔧 **Platform-Agnostic Design**: Works with Twitter, TikTok, Instagram, and custom platforms
- 📊 **Social Simulation**: Generate realistic social media activity and user behavior
- 🎯 **Twitter/X API v2 Compatible**: Follows the official API data structure
- 🚀 **Zero Dependencies**: Uses only Python standard library
- 📈 **Rich Analytics**: Track engagement, virality, and user behavior patterns
- 🔄 **Flexible Import**: Use as a module (`import feed`) for your projects

## Installation

### As a Module (Recommended)

```python
# Clone the repository
git clone https://github.com/yourusername/feed.git
cd Feed

# Install as a package
pip install -e .

# Or install directly
pip install .
```

### Direct Usage

```python
# No installation needed - just import
import sys
sys.path.append('/path/to/Feed')
import feed
```

## Quick Start

### Basic Usage

```python
import feed

# Create a simple feed
my_feed = feed.create_feed(
    text="Hello World! #FirstPost",
    author_id="user123",
    platform="twitter"
)

# Save the feed
filepath = feed.save_feed(my_feed)
print(f"Saved to: {filepath}")
```

### Social Media Simulation

```python
import feed

# Create a social simulator
simulator = feed.SocialSimulator()

# Generate realistic social media activity
feeds = simulator.generate_sample_feeds(count=100, platform="twitter")

# Run a full simulation
config = feed.SimulationConfig(
    num_users=50,
    num_feeds=500,
    duration_hours=24,
    platform="twitter"
)
simulator = feed.SocialSimulator(config)
feeds, stats = simulator.simulate_activity()

# Save simulation results
result = simulator.save_simulation()
print(f"Generated {stats['total_feeds']} feeds with {stats['total_engagement']} engagements")
```

### Creating Threads

```python
import feed

# Create a thread of connected posts
thread_texts = [
    "🧵 Let's talk about social simulation (1/3)",
    "The feed module makes it easy to generate realistic data (2/3)",
    "Perfect for testing and research! (3/3)"
]

manager = feed.FeedManager()
thread = feed.create_thread(thread_texts, "author123", manager, "twitter")
```

## Module Structure

```
Feed/
├── __init__.py          # Module entry point
├── feed_models.py       # Core data models
├── feed_utils.py        # Utility functions
├── simulation.py        # Social simulation engine
├── example_simulation.py # Usage examples
└── setup.py            # Package configuration
```

## Core Components

### Feed Types
- `POST` - Standard text posts
- `VIDEO` - Video content
- `IMAGE_POST` - Image-focused posts
- `STORY` - Ephemeral content
- `REEL` - Short videos
- `THREAD` - Connected posts

### Simulation Features
- **User Behavior Modeling**: Influencers, high/medium/low activity users
- **Content Generation**: Realistic text, hashtags, mentions, URLs
- **Engagement Simulation**: Likes, reposts, replies with viral growth
- **Platform-Specific**: Customize behavior per platform
- **Time-Based**: Simulate activity over hours/days

## Advanced Examples

### Influencer Simulation

```python
config = feed.SimulationConfig(
    num_users=20,
    num_feeds=200,
    like_rate=0.30,  # Higher engagement
    with_media_rate=0.70,  # More visual content
)

simulator = feed.SocialSimulator(config)
feeds, stats = simulator.simulate_activity()
```

### Cross-Platform Comparison

```python
platforms = ["twitter", "tiktok", "instagram"]

for platform in platforms:
    simulator = feed.SocialSimulator()
    feeds = simulator.generate_sample_feeds(50, platform)
    # Analyze platform-specific patterns
```

## Data Structure

# Information about a Tweet

A Tweet (now called a “Post” on X) is a JSON object. In **X API v2**, you choose which fields you want with the `tweet.fields` parameter (by default you only get `id` and `text`, plus `edit_history_tweet_ids` for posts created on/after Sep 29, 2022). Related objects (user, media, polls, places, referenced posts) come back via `expansions` and appear under `includes`. ([X Developer Platform][1])

# Official docs you’ll want

* **Get Posts by IDs** (shows the allowed `tweet.fields`, `expansions`, etc.). ([X Developer Platform][2])
* **v2 “Fields” fundamentals** (explains the fields/expansions model and defaults). ([X Developer Platform][1])
* **Legacy v1.1 Tweet data dictionary** (full legacy field list; still useful if you’re reading old payloads). ([X Developer][3])
* **v1.1 → v2 migration notes** (differences like `data` vs `statuses`, `like` terminology, etc.). ([X Developer][4])
* **Entities** (hashtags, mentions, urls, media, polls) and **Geo/Place** object docs. ([X Developer][5])
* **Edited post metadata** (adds `edit_history_tweet_ids` and `edit_controls`). ([X Developer][6])

# Common v2 Tweet fields (pick via `tweet.fields`)

* `id`, `text` — always returned (plus `edit_history_tweet_ids` for newer posts). ([X Developer Platform][1])
* `created_at`, `author_id`, `conversation_id`, `in_reply_to_user_id`
* `referenced_tweets` (replied_to / quoted / retweeted)
* `entities` (hashtags, mentions, urls), `attachments` (media/poll ids), `geo` (place id / coords)
* `public_metrics` (retweet, reply, like, quote counts)
* `context_annotations`, `possibly_sensitive`, `lang`, `source`, `reply_settings`, `withheld`, `edit_controls`
  (See the endpoint page for the exact allowed list.) ([X Developer Platform][2])

# Minimal example (v2 style)

```json
{
  "data": [
    {
      "id": "1871234567890",
      "text": "hello, world",
      "author_id": "12345",
      "created_at": "2025-10-28T15:32:10.000Z",
      "conversation_id": "1871234567890",
      "referenced_tweets": [{"type": "replied_to", "id": "1871234500000"}],
      "entities": {"hashtags": [{"tag": "Example"}], "mentions": [{"username": "someone"}]},
      "attachments": {"media_keys": ["3_1111111111111111111"]},
      "geo": {"place_id": "01a9a39529b27f36"},
      "public_metrics": {"retweet_count": 2, "reply_count": 1, "like_count": 7, "quote_count": 0},
      "edit_history_tweet_ids": ["1871234567890"]
    }
  ],
  "includes": {
    "users": [{"id": "12345", "username": "alice"}],
    "media": [{"media_key": "3_1111111111111111111", "type": "photo"}],
    "places": [{"id": "01a9a39529b27f36", "full_name": "NYC, NY"}]
  }
}
```

# How to request those fields

Use **GET `/2/tweets`** with `ids`, add `tweet.fields` and any `expansions` (e.g., `author_id`, `attachments.media_keys`, `geo.place_id`) and corresponding `user.fields`, `media.fields`, `place.fields`, `poll.fields`. The “Get Posts by IDs” page lists the valid values and examples. ([X Developer Platform][2])

If you tell me what you’re building (analytics vs. rendering vs. storage), I can suggest a minimal field set and a ready-to-run request.

[1]: https://docs.x.com/x-api/fundamentals/fields?utm_source=chatgpt.com "Fields"
[2]: https://docs.x.com/x-api/posts/get-posts-by-ids?utm_source=chatgpt.com "Get Posts by IDs"
[3]: https://developer.x.com/en/docs/x-api/v1/data-dictionary/object-model/tweet?utm_source=chatgpt.com "Tweet object | Docs | Twitter Developer Platform - X"
[4]: https://developer.x.com/en/docs/x-api/tweets/lookup/migrate/standard-to-twitter-api-v2?utm_source=chatgpt.com "Tweet lookup standard v1.1 to v2 migration guide | Docs"
[5]: https://developer.x.com/en/docs/x-api/v1/data-dictionary/object-model/entities?utm_source=chatgpt.com "Entities object | Docs | Twitter Developer Platform"
[6]: https://developer.x.com/en/blog/product-news/2022/supporting-edit-post-functionality?utm_source=chatgpt.com "Supporting Edit Tweet functionality with new API metadata"
