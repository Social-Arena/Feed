## Quick Start Guide

### Installation

```bash
cd feed
pip install -e .
```

### 1. Create Your First Tweet

```python
import feed

tweet = feed.create_tweet(
    text="My first tweet with the Feed package! #Python",
    author_id="user_001"
)

print(tweet.text)
print(tweet.id)
```

### 2. Extract Entities

```python
import feed

text = "Hello @twitter! Check out #Python https://python.org"
entities = feed.extract_entities(text)

print(f"Hashtags: {[h.tag for h in entities.hashtags]}")
print(f"Mentions: {[m.username for m in entities.mentions]}")
print(f"URLs: {len(entities.urls)}")
```

### 3. Run a Quick Simulation

```python
import feed

# Simulate 50 tweets from 20 users
tweets, stats = feed.simulate_twitter(num_tweets=50, num_users=20)

print(f"Generated {len(tweets)} tweets")
print(f"Total likes: {sum(t.public_metrics.like_count for t in tweets)}")
print(f"Total retweets: {sum(t.public_metrics.retweet_count for t in tweets)}")
```

### 4. Advanced Simulation

```python
import feed

# Custom configuration
config = feed.SimulationConfig(
    num_users=100,
    num_tweets=500,
    duration_hours=24,
    like_rate=0.25,  # 25% like rate
    retweet_rate=0.08,  # 8% retweet rate
)

# Run simulation
simulator = feed.TwitterSimulator(config)
tweets, stats = simulator.simulate()

# Show top tweets
top_tweets = sorted(tweets, key=lambda t: t.public_metrics.like_count, reverse=True)[:5]
for i, tweet in enumerate(top_tweets, 1):
    print(f"{i}. {tweet.text}")
    print(f"   Likes: {tweet.public_metrics.like_count}")
```

### 5. Save and Load Tweets

```python
import feed

manager = feed.FeedManager(storage_dir="./my_tweets")

# Create and save
tweet = manager.create_feed(
    text="Saving this tweet!",
    author_id="user_123"
)
filepath = manager.save_feed(tweet)

# Load it back
loaded = manager.load_feed(filepath)
print(loaded.text)

# Load all tweets
all_tweets = manager.load_all_feeds()
print(f"Found {len(all_tweets)} tweets")
```

### 6. Search Tweets

```python
import feed

manager = feed.FeedManager()

# Search by text
python_tweets = manager.search_feeds(text_contains="Python")

# Search by author
user_tweets = manager.search_feeds(author_id="user_123")

# Search by type
replies = manager.search_feeds(feed_type=feed.FeedType.REPLY)
```

### Next Steps

- Check out `examples/basic_usage.py` for more examples
- Run `examples/simulation_demo.py` for simulation scenarios
- Read `docs/USAGE.md` for comprehensive documentation
- Explore the `feed/` package structure to understand the architecture

### Package Structure Overview

```python
import feed

# Models
feed.Feed              # Main tweet data structure
feed.FeedType          # POST, REPLY, QUOTE, RETWEET
feed.PublicMetrics     # Engagement metrics
feed.User              # User model

# Utilities
feed.FeedManager       # CRUD operations
feed.extract_entities  # Extract hashtags/mentions/URLs

# Simulation
feed.TwitterSimulator  # Main simulator
feed.SimulationConfig  # Configuration
feed.ContentGenerator  # Content creation
```

### Common Patterns

**Create a reply:**

```python
manager = feed.FeedManager()

original = manager.create_feed(text="Original tweet", author_id="user_1")
reply = manager.create_feed(
    text="@user_1 This is a reply",
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

**Create a quote tweet:**

```python
quote = manager.create_feed(
    text="This is brilliant!",
    author_id="user_3",
    feed_type=feed.FeedType.QUOTE,
    referenced_feeds=[
        feed.ReferencedFeed(
            type=feed.ReferencedFeedType.QUOTED.value,
            id=original.id
        )
    ]
)
```

**Set custom metrics:**

```python
tweet.public_metrics = feed.PublicMetrics(
    like_count=100,
    retweet_count=25,
    reply_count=10,
    quote_count=5,
    bookmark_count=15,
    impression_count=2000
)
```

### Tips

1. **Storage**: Tweets are saved as individual JSON files in the `feeds/` directory
2. **IDs**: Tweet IDs are automatically generated with timestamps
3. **Entities**: Use `extract_entities()` to automatically parse hashtags, mentions, and URLs
4. **Simulation**: Adjust `SimulationConfig` parameters to tune realism
5. **Testing**: Run `python tests/test_feed.py` to verify everything works

Happy tweeting! 🐦

