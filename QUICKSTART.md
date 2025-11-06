# Quick Start Guide - Feed Data Structure Library

## Installation

```bash
cd Feed
pip install -e .
```

## Basic Usage

### 1. Create Your First Tweet

```python
import feed

manager = feed.FeedManager()

tweet = manager.create_feed(
    text="My first tweet with Feed! #Python",
    author_id="user_001"
)

print(f"Created tweet: {tweet.id}")
print(f"Text: {tweet.text}")
```

### 2. Extract Entities from Text

```python
import feed

text = "Hello @twitter! Check out #Python at https://python.org"
entities = feed.extract_entities(text)

if entities:
    print(f"Hashtags: {[h.tag for h in entities.hashtags]}")
    print(f"Mentions: {[m.username for m in entities.mentions]}")
    print(f"URLs: {len(entities.urls)}")
```

**Output:**
```
Hashtags: ['Python']
Mentions: ['twitter']
URLs: 1
```

### 3. Create a Reply

```python
import feed

manager = feed.FeedManager()

# Original tweet
original = manager.create_feed(
    text="What's everyone building today?",
    author_id="user_1"
)

# Reply to it
reply = manager.create_feed(
    text="@user_1 Working on data structures!",
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

print(f"Reply conversation ID: {reply.conversation_id}")
```

### 4. Save and Load Tweets

```python
import feed

manager = feed.FeedManager(storage_dir="./my_tweets")

# Create and save
tweet = manager.create_feed(
    text="Saving this tweet!",
    author_id="user_123"
)
filepath = manager.save_feed(tweet)
print(f"Saved to: {filepath}")

# Load it back
loaded = manager.load_feed(filepath)
print(f"Loaded: {loaded.text}")

# Load all tweets
all_tweets = manager.load_all_feeds()
print(f"Total tweets: {len(all_tweets)}")
```

### 5. Search Tweets

```python
import feed

manager = feed.FeedManager()

# Search by text
python_tweets = manager.search_feeds(text_contains="Python")

# Search by author
user_tweets = manager.search_feeds(author_id="user_123")

# Search by type
replies = manager.search_feeds(feed_type=feed.FeedType.REPLY)

print(f"Found {len(python_tweets)} tweets about Python")
```

### 6. Add Engagement Metrics

```python
import feed

manager = feed.FeedManager()

tweet = manager.create_feed(
    text="This tweet went viral!",
    author_id="user_456"
)

# Set metrics
tweet.public_metrics = feed.PublicMetrics(
    like_count=1500,
    retweet_count=450,
    reply_count=230,
    quote_count=85,
    bookmark_count=120,
    impression_count=50000
)

print(f"Likes: {tweet.public_metrics.like_count}")
print(f"Retweets: {tweet.public_metrics.retweet_count}")
```

### 7. Create a Quote Tweet

```python
import feed

manager = feed.FeedManager()

original = manager.create_feed(
    text="Data structures are important!",
    author_id="user_1"
)

quote = manager.create_feed(
    text="Absolutely agree! Here's why...",
    author_id="user_2",
    feed_type=feed.FeedType.QUOTE,
    referenced_feeds=[
        feed.ReferencedFeed(
            type=feed.ReferencedFeedType.QUOTED.value,
            id=original.id
        )
    ]
)
```

### 8. Work with Users

```python
import feed

# Create a sample user
user = feed.create_sample_user(
    user_id="12345",
    username="johndoe",
    name="John Doe"
)

print(f"User: @{user.username} ({user.name})")
print(f"Followers: {user.public_metrics['followers_count']}")
print(f"Verified: {user.verified}")
```

### 9. Serialize to JSON

```python
import feed
import json

manager = feed.FeedManager()
tweet = manager.create_feed(
    text="Converting to JSON",
    author_id="user_1"
)

# Convert to dict
data = tweet.to_dict()

# Save as JSON
with open('tweet.json', 'w') as f:
    json.dump(data, f, indent=2)

# Load from JSON
with open('tweet.json', 'r') as f:
    data = json.load(f)
    loaded_tweet = feed.Feed.from_dict(data)
```

## Building a Simulator

Feed provides the data structures. Here's a simple example of building on top:

```python
import feed
import random

class SimpleTwitterSimulator:
    def __init__(self):
        self.manager = feed.FeedManager()
        self.tweets = []
    
    def generate_tweet(self, author_id, text):
        """Generate a tweet with realistic structure"""
        tweet = self.manager.create_feed(
            text=text,
            author_id=author_id
        )
        
        # Extract entities
        tweet.entities = feed.extract_entities(text)
        
        # Add simulated metrics
        tweet.public_metrics = feed.PublicMetrics(
            like_count=random.randint(0, 100),
            retweet_count=random.randint(0, 20),
            reply_count=random.randint(0, 10)
        )
        
        self.tweets.append(tweet)
        return tweet
    
    def generate_reply(self, original_tweet, author_id, text):
        """Generate a reply to an existing tweet"""
        reply = self.manager.create_feed(
            text=text,
            author_id=author_id,
            feed_type=feed.FeedType.REPLY,
            conversation_id=original_tweet.conversation_id,
            in_reply_to_user_id=original_tweet.author_id,
            referenced_feeds=[
                feed.ReferencedFeed(
                    type=feed.ReferencedFeedType.REPLIED_TO.value,
                    id=original_tweet.id
                )
            ]
        )
        
        reply.entities = feed.extract_entities(text)
        reply.public_metrics = feed.PublicMetrics(
            like_count=random.randint(0, 50),
            retweet_count=random.randint(0, 10),
            reply_count=random.randint(0, 5)
        )
        
        self.tweets.append(reply)
        return reply

# Usage
sim = SimpleTwitterSimulator()

# Generate tweets
tweet1 = sim.generate_tweet("user_1", "Hello Twitter! #Python")
tweet2 = sim.generate_tweet("user_2", "Building cool stuff! #Coding")

# Generate replies
reply = sim.generate_reply(tweet1, "user_3", "@user_1 Great post!")

print(f"Generated {len(sim.tweets)} tweets")
```

## Common Patterns

### Create a Thread

```python
def create_thread(texts, author_id, manager):
    """Create a thread of connected tweets"""
    thread = []
    conversation_id = None
    
    for i, text in enumerate(texts):
        if i == 0:
            # First tweet
            tweet = manager.create_feed(
                text=text,
                author_id=author_id
            )
            conversation_id = tweet.id
        else:
            # Reply to previous
            tweet = manager.create_feed(
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
        
        tweet.entities = feed.extract_entities(text)
        thread.append(tweet)
    
    return thread

# Usage
manager = feed.FeedManager()
thread = create_thread([
    "1/ Here's an important thread about data structures",
    "2/ First, let's talk about the Feed model...",
    "3/ It follows the Twitter API v2 structure exactly"
], "user_123", manager)
```

## Tips

1. **Always extract entities** after setting tweet text
2. **Use FeedManager** for consistent ID generation
3. **Set conversation_id** for proper threading
4. **Save tweets** using FeedManager for consistent formatting
5. **Use type hints** - Feed models are fully typed

## Next Steps

- Read `README.md` for comprehensive documentation
- Check `tests/test_feed.py` for more examples
- See `docs/USAGE.md` for advanced usage
- Build your simulator on top of Feed!

---

**Happy building! 🐦**
