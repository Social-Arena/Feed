# Social Arena - Feed 🐦

A comprehensive Twitter/X data structure library providing clean, type-safe models for social media content. Built as the foundational data layer for the Social Arena simulation ecosystem.

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Social-Arena/Feed.git
cd Feed
pip install -e .
```

### Basic Usage

```python
import feed

# Create a feed manager
manager = feed.FeedManager()

# Create a tweet
tweet = manager.create_feed(
    text="Building the future of social media simulation! #SocialArena #AI",
    author_id="user_123"
)

# Extract entities automatically
entities = feed.extract_entities(tweet.text)
print(f"Hashtags: {[h.tag for h in entities.hashtags]}")
print(f"Mentions: {[m.username for m in entities.mentions]}")
```

## 📊 Core Features

### 🏗️ Twitter API v2 Compatible Data Models
- **Complete Tweet Structure**: All fields from Twitter API v2
- **Type Safety**: Full Python type hints throughout
- **Zero Dependencies**: Pure Python standard library
- **JSON Serialization**: Direct compatibility with Twitter API responses

### 🔧 Essential Tweet Operations
- **Feed Creation**: Programmatic tweet generation with validation
- **Entity Extraction**: Automatic hashtag, mention, and URL parsing
- **Relationship Management**: Reply chains, quote tweets, retweets
- **Metrics Tracking**: Engagement and performance metrics
- **Content Validation**: Tweet length, character limits, format validation

### 💾 Data Management
- **Persistent Storage**: JSON file-based storage system
- **Bulk Operations**: Efficient batch loading and saving
- **Search Capabilities**: Query tweets by content, author, type
- **Data Integrity**: Validation and consistency checks

## 🛠️ System Architecture

### Package Structure

```
feed/
├── models/                    # Core data models
│   ├── feed.py               # Main Feed (Tweet) entity
│   ├── entities.py           # Hashtags, mentions, URLs, cashtags
│   ├── metrics.py            # Public and private metrics
│   ├── references.py         # Tweet references (replies, quotes)
│   ├── user.py               # User profile model
│   ├── media.py              # Media attachments
│   └── context_annotations.py # Content classification
├── utils/                     # Utility functions
│   ├── manager.py            # FeedManager for CRUD operations
│   ├── entities.py           # Entity extraction and validation
│   ├── generators.py         # ID and timestamp generation
│   ├── validators.py         # Data validation utilities
│   └── serializers.py        # JSON serialization helpers
├── feeds/                     # Pre-built feed collections
│   ├── trending/             # Trending content datasets
│   ├── templates/            # Tweet templates
│   └── samples/              # Sample data for testing
├── examples/                  # Usage examples
│   ├── basic_usage.py        # Getting started examples
│   ├── advanced_features.py  # Complex operations
│   └── integration_demo.py   # System integration
├── tests/                     # Comprehensive test suite
│   ├── test_models.py        # Model validation tests
│   ├── test_entities.py      # Entity extraction tests
│   ├── test_manager.py       # Manager functionality tests
│   └── test_integration.py   # End-to-end tests
└── docs/                      # Documentation
    ├── USAGE.md              # Detailed usage guide
    ├── API.md                # Complete API reference
    └── EXAMPLES.md           # Extended examples
```

### Core Data Models

#### Feed (Tweet) Model

```python
@dataclass
class Feed:
    # Basic tweet information
    id: str                                # Unique tweet ID (snowflake)
    text: str                              # Tweet content (max 280 chars)
    author_id: str                         # Tweet author's user ID
    created_at: str                        # ISO 8601 timestamp
    
    # Tweet type and context
    feed_type: FeedType                    # POST, REPLY, QUOTE, RETWEET
    conversation_id: Optional[str]         # Thread/conversation ID
    in_reply_to_user_id: Optional[str]    # Original author for replies
    
    # References and relationships
    referenced_feeds: List[ReferencedFeed] # Linked tweets (replies, quotes)
    
    # Content analysis
    entities: Optional[Entities]           # Extracted entities
    context_annotations: List[ContextAnnotation] # Content classification
    
    # Engagement metrics
    public_metrics: PublicMetrics          # Like, retweet, reply counts
    private_metrics: Optional[PrivateMetrics] # Impression, profile clicks
    
    # Metadata
    lang: str                              # Language code (ISO 639-1)
    source: str                            # Client application
    possibly_sensitive: bool               # Content sensitivity flag
    reply_settings: ReplySettings          # Who can reply
```

#### Entity Models

```python
@dataclass
class HashtagEntity:
    start: int          # Character start position
    end: int            # Character end position  
    tag: str            # Hashtag text (without #)

@dataclass
class MentionEntity:
    start: int          # Character start position
    end: int            # Character end position
    username: str       # Username (without @)
    id: Optional[str]   # User ID if available

@dataclass
class UrlEntity:
    start: int              # Character start position
    end: int                # Character end position
    url: str                # Shortened URL (t.co)
    expanded_url: str       # Full expanded URL
    display_url: str        # Display-friendly URL
    unwound_url: Optional[str] # Final destination URL
```

#### Metrics Models

```python
@dataclass
class PublicMetrics:
    like_count: int                    # Number of likes
    retweet_count: int                 # Number of retweets
    reply_count: int                   # Number of replies
    quote_count: int                   # Number of quote tweets
    bookmark_count: int                # Number of bookmarks
    impression_count: Optional[int]    # View count (if available)

@dataclass
class PrivateMetrics:
    impression_count: int              # Total impressions
    profile_clicks: int                # Profile view clicks
    url_link_clicks: int               # URL click count
    user_profile_clicks: int           # Author profile clicks
```

## 🧰 Advanced Usage Examples

### Creating Complex Tweet Structures

```python
import feed
from datetime import datetime

manager = feed.FeedManager()

# Create original tweet
original = manager.create_feed(
    text="What's everyone working on this weekend? #coding #projects",
    author_id="user_123",
    feed_type=feed.FeedType.POST
)

# Create a reply with mentions and URLs
reply = manager.create_feed(
    text="@user_123 Working on an AI simulation platform! Check it out: https://socialarena.com #AI #simulation",
    author_id="user_456",
    feed_type=feed.FeedType.REPLY,
    conversation_id=original.id,
    in_reply_to_user_id="user_123",
    referenced_feeds=[
        feed.ReferencedFeed(
            type=feed.ReferencedFeedType.REPLIED_TO.value,
            id=original.id
        )
    ]
)

# Create a quote tweet
quote = manager.create_feed(
    text="This is exactly the kind of innovation we need in social media research!",
    author_id="user_789",
    feed_type=feed.FeedType.QUOTE,
    conversation_id=original.id,
    referenced_feeds=[
        feed.ReferencedFeed(
            type=feed.ReferencedFeedType.QUOTED.value,
            id=reply.id
        )
    ]
)

print(f"Created thread with {len([original, reply, quote])} tweets")
```

### Advanced Entity Processing

```python
import feed

# Complex text with multiple entity types
text = """
🚀 Exciting news! @socialarena just launched their new AI platform! 

Check it out: https://socialarena.com/platform 
More details: https://blog.socialarena.com/launch

#AI #MachineLearning #SocialMedia #Innovation #TechLaunch
$TSLA $AAPL might find this interesting 💡

Join the beta: beta@socialarena.com
"""

# Extract all entities
entities = feed.extract_entities(text)

# Analyze extracted entities
print(f"Found {len(entities.hashtags)} hashtags:")
for hashtag in entities.hashtags:
    print(f"  #{hashtag.tag} at position {hashtag.start}-{hashtag.end}")

print(f"\nFound {len(entities.mentions)} mentions:")
for mention in entities.mentions:
    print(f"  @{mention.username} at position {mention.start}-{mention.end}")

print(f"\nFound {len(entities.urls)} URLs:")
for url in entities.urls:
    print(f"  {url.display_url} -> {url.expanded_url}")

print(f"\nFound {len(entities.cashtags)} cashtags:")
for cashtag in entities.cashtags:
    print(f"  ${cashtag.tag} at position {cashtag.start}-{cashtag.end}")
```

### Engagement Metrics and Analytics

```python
import feed

manager = feed.FeedManager()

# Create tweet with comprehensive metrics
viral_tweet = manager.create_feed(
    text="Just discovered something amazing about social media algorithms! 🤯 #Algorithm #SocialMedia",
    author_id="influencer_user"
)

# Set realistic engagement metrics
viral_tweet.public_metrics = feed.PublicMetrics(
    like_count=15_420,
    retweet_count=3_891,
    reply_count=892,
    quote_count=1_247,
    bookmark_count=5_632,
    impression_count=847_293
)

# Add private metrics (for analytics)
viral_tweet.private_metrics = feed.PrivateMetrics(
    impression_count=847_293,
    profile_clicks=12_847,
    url_link_clicks=0,  # No URLs in this tweet
    user_profile_clicks=8_934
)

# Calculate engagement rates
total_engagements = (
    viral_tweet.public_metrics.like_count +
    viral_tweet.public_metrics.retweet_count +
    viral_tweet.public_metrics.reply_count +
    viral_tweet.public_metrics.quote_count
)

engagement_rate = total_engagements / viral_tweet.public_metrics.impression_count
print(f"Engagement rate: {engagement_rate:.2%}")

# Save for analysis
filepath = manager.save_feed(viral_tweet)
print(f"Saved viral tweet to: {filepath}")
```

### Bulk Data Operations

```python
import feed

manager = feed.FeedManager(storage_dir="./simulation_data")

# Create a batch of related tweets
tweet_batch = []

topics = ["#AI", "#MachineLearning", "#DataScience", "#TechNews"]
authors = [f"user_{i}" for i in range(1, 11)]

for i in range(100):
    topic = topics[i % len(topics)]
    author = authors[i % len(authors)]
    
    tweet = manager.create_feed(
        text=f"Interesting developments in {topic} today! What do you think about the latest trends? #{i}",
        author_id=author
    )
    
    # Add realistic engagement metrics
    tweet.public_metrics = feed.PublicMetrics(
        like_count=random.randint(5, 500),
        retweet_count=random.randint(0, 50),
        reply_count=random.randint(0, 25),
        quote_count=random.randint(0, 10),
        bookmark_count=random.randint(0, 100),
        impression_count=random.randint(1000, 10000)
    )
    
    tweet_batch.append(tweet)

# Save all tweets
for tweet in tweet_batch:
    manager.save_feed(tweet)

print(f"Created and saved {len(tweet_batch)} tweets")

# Search and analyze
ai_tweets = manager.search_feeds(text_contains="#AI")
print(f"Found {len(ai_tweets)} tweets about AI")

# Calculate average engagement
total_likes = sum(tweet.public_metrics.like_count for tweet in ai_tweets)
avg_likes = total_likes / len(ai_tweets) if ai_tweets else 0
print(f"Average likes for AI tweets: {avg_likes:.1f}")
```

### Integration with External Systems

```python
import feed
import json
from typing import List, Dict

class SocialArenaIntegration:
    """Example integration with Social Arena simulation system"""
    
    def __init__(self):
        self.feed_manager = feed.FeedManager()
        self.simulation_data = []
    
    def import_from_twitter_api(self, twitter_response: Dict) -> feed.Feed:
        """Convert Twitter API response to Feed model"""
        
        # Create feed from Twitter API data
        tweet = feed.Feed.from_dict(twitter_response)
        
        # Save to our system
        self.feed_manager.save_feed(tweet)
        
        return tweet
    
    def export_for_recommendation_engine(self, user_id: str) -> List[Dict]:
        """Export user's tweets for recommendation system"""
        
        # Get all tweets from user
        user_tweets = self.feed_manager.search_feeds(author_id=user_id)
        
        # Format for recommendation engine
        recommendation_data = []
        for tweet in user_tweets:
            data = {
                "content_id": tweet.id,
                "text": tweet.text,
                "entities": {
                    "hashtags": [h.tag for h in tweet.entities.hashtags] if tweet.entities else [],
                    "mentions": [m.username for m in tweet.entities.mentions] if tweet.entities else []
                },
                "engagement": {
                    "likes": tweet.public_metrics.like_count,
                    "retweets": tweet.public_metrics.retweet_count,
                    "replies": tweet.public_metrics.reply_count
                },
                "timestamp": tweet.created_at
            }
            recommendation_data.append(data)
        
        return recommendation_data
    
    def generate_simulation_feeds(self, num_feeds: int = 1000) -> List[feed.Feed]:
        """Generate synthetic feeds for simulation"""
        
        feeds = []
        
        # Generate diverse content
        for i in range(num_feeds):
            # Create realistic tweet content
            tweet_text = self._generate_realistic_content(i)
            
            tweet = self.feed_manager.create_feed(
                text=tweet_text,
                author_id=f"sim_user_{i % 100}"  # 100 simulated users
            )
            
            # Add realistic metrics
            tweet.public_metrics = self._generate_realistic_metrics()
            
            feeds.append(tweet)
        
        return feeds
    
    def _generate_realistic_content(self, index: int) -> str:
        """Generate realistic tweet content for simulation"""
        
        templates = [
            "Just discovered an amazing new {topic}! {hashtag} #innovation",
            "Can't believe how much {topic} has evolved. What's next? {hashtag}",
            "Hot take: {topic} will revolutionize how we think about {concept}. {hashtag}",
            "Working late on some exciting {topic} projects. {hashtag} #hustle",
            "Anyone else excited about the future of {topic}? {hashtag} #futurism"
        ]
        
        topics = ["AI", "blockchain", "quantum computing", "biotech", "renewable energy"]
        concepts = ["social media", "data privacy", "automation", "creativity", "connection"]
        hashtags = ["#TechTrends", "#Innovation", "#FutureThinking", "#DigitalAge", "#Progress"]
        
        template = templates[index % len(templates)]
        topic = topics[index % len(topics)]
        concept = concepts[index % len(concepts)]
        hashtag = hashtags[index % len(hashtags)]
        
        return template.format(topic=topic, concept=concept, hashtag=hashtag)
    
    def _generate_realistic_metrics(self) -> feed.PublicMetrics:
        """Generate realistic engagement metrics"""
        import random
        
        # Simulate power-law distribution for engagement
        base_engagement = random.randint(1, 100)
        
        return feed.PublicMetrics(
            like_count=base_engagement * random.randint(1, 10),
            retweet_count=base_engagement * random.randint(0, 3),
            reply_count=base_engagement * random.randint(0, 2),
            quote_count=base_engagement * random.randint(0, 1),
            bookmark_count=base_engagement * random.randint(0, 5),
            impression_count=base_engagement * random.randint(50, 500)
        )

# Example usage
integration = SocialArenaIntegration()

# Generate simulation data
simulation_feeds = integration.generate_simulation_feeds(100)
print(f"Generated {len(simulation_feeds)} simulation feeds")

# Export for other systems
sample_user = "sim_user_1"
recommendation_data = integration.export_for_recommendation_engine(sample_user)
print(f"Exported {len(recommendation_data)} tweets for recommendations")
```

## 🔧 Configuration and Customization

### Custom Feed Types

```python
import feed
from enum import Enum

class CustomFeedType(Enum):
    """Extended feed types for specialized use cases"""
    ANNOUNCEMENT = "announcement"
    POLL = "poll"
    THREAD_START = "thread_start"
    THREAD_CONTINUATION = "thread_continuation"
    PROMOTIONAL = "promotional"
    NEWS_UPDATE = "news_update"

# Create custom feed with extended type
manager = feed.FeedManager()

announcement = manager.create_feed(
    text="🎉 Major product announcement coming next week! Stay tuned for something revolutionary in social media simulation! #BigNews #SocialArena",
    author_id="official_account",
    feed_type=CustomFeedType.ANNOUNCEMENT.value  # Use custom type
)

# Add custom metadata
announcement.custom_metadata = {
    "announcement_type": "product_launch",
    "priority": "high",
    "target_audience": ["developers", "researchers", "data_scientists"],
    "campaign_id": "launch_2024_q4"
}
```

### Advanced Validation Rules

```python
import feed
from feed.utils.validators import ValidationRule, ValidationError

class CustomValidationRule(ValidationRule):
    """Custom validation for business requirements"""
    
    def validate(self, tweet: feed.Feed) -> None:
        # Custom business logic validation
        if tweet.feed_type == "promotional":
            # Promotional tweets must have specific hashtags
            required_tags = ["#ad", "#sponsored", "#promotion"]
            if not tweet.entities or not tweet.entities.hashtags:
                raise ValidationError("Promotional tweets must include disclosure hashtags")
            
            tweet_tags = [h.tag.lower() for h in tweet.entities.hashtags]
            if not any(tag.lower() in tweet_tags for tag in required_tags):
                raise ValidationError("Promotional tweets must include disclosure hashtags")
        
        # Check content quality
        if len(tweet.text.split()) < 3:
            raise ValidationError("Tweets must contain at least 3 words")
        
        # Prevent spam patterns
        if tweet.text.count('!') > 3:
            raise ValidationError("Too many exclamation marks detected")

# Register custom validation
manager = feed.FeedManager()
manager.add_validation_rule(CustomValidationRule())

# Validation will be applied automatically
try:
    spam_tweet = manager.create_feed(
        text="BUY NOW!!!! Amazing deal!!!!", 
        author_id="spam_account"
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## 📈 Performance and Optimization

### Efficient Batch Processing

```python
import feed
import time
from concurrent.futures import ProcessPoolExecutor

def process_tweet_batch(tweets_data: List[Dict]) -> List[feed.Feed]:
    """Process tweets in parallel for better performance"""
    
    def create_single_tweet(tweet_data):
        manager = feed.FeedManager()
        return manager.create_feed(**tweet_data)
    
    with ProcessPoolExecutor() as executor:
        tweets = list(executor.map(create_single_tweet, tweets_data))
    
    return tweets

# Example: Process 1000 tweets efficiently
start_time = time.time()

tweet_data_list = [
    {
        "text": f"Sample tweet #{i} with various content and #hashtags",
        "author_id": f"user_{i % 100}"
    }
    for i in range(1000)
]

processed_tweets = process_tweet_batch(tweet_data_list)

end_time = time.time()
print(f"Processed {len(processed_tweets)} tweets in {end_time - start_time:.2f} seconds")
```

### Memory-Efficient Large Dataset Handling

```python
import feed
from typing import Iterator

class LargeFeedProcessor:
    """Handle large datasets without loading everything into memory"""
    
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        self.manager = feed.FeedManager(storage_dir=storage_dir)
    
    def stream_feeds(self, batch_size: int = 100) -> Iterator[List[feed.Feed]]:
        """Stream feeds in batches to avoid memory issues"""
        
        all_files = self.manager.list_feed_files()
        
        for i in range(0, len(all_files), batch_size):
            batch_files = all_files[i:i + batch_size]
            batch_feeds = []
            
            for file_path in batch_files:
                try:
                    feed_obj = self.manager.load_feed(file_path)
                    batch_feeds.append(feed_obj)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue
            
            yield batch_feeds
    
    def analyze_engagement_trends(self) -> Dict[str, float]:
        """Analyze engagement across large dataset efficiently"""
        
        total_tweets = 0
        total_likes = 0
        total_retweets = 0
        hashtag_counts = {}
        
        # Process in batches to avoid memory issues
        for batch in self.stream_feeds(batch_size=500):
            for tweet in batch:
                total_tweets += 1
                total_likes += tweet.public_metrics.like_count
                total_retweets += tweet.public_metrics.retweet_count
                
                # Count hashtags
                if tweet.entities and tweet.entities.hashtags:
                    for hashtag in tweet.entities.hashtags:
                        hashtag_counts[hashtag.tag] = hashtag_counts.get(hashtag.tag, 0) + 1
        
        # Calculate averages
        avg_likes = total_likes / total_tweets if total_tweets > 0 else 0
        avg_retweets = total_retweets / total_tweets if total_tweets > 0 else 0
        
        # Top hashtags
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_tweets": total_tweets,
            "average_likes": avg_likes,
            "average_retweets": avg_retweets,
            "top_hashtags": top_hashtags
        }

# Example usage for large datasets
processor = LargeFeedProcessor("./large_dataset")
trends = processor.analyze_engagement_trends()
print(f"Analyzed {trends['total_tweets']} tweets")
print(f"Average engagement: {trends['average_likes']:.1f} likes, {trends['average_retweets']:.1f} retweets")
```

## 🧪 Testing and Quality Assurance

### Comprehensive Test Suite

```python
import feed
import pytest
from datetime import datetime, timezone

class TestFeedSystem:
    """Comprehensive test suite for Feed system"""
    
    def test_basic_feed_creation(self):
        """Test basic tweet creation functionality"""
        manager = feed.FeedManager()
        
        tweet = manager.create_feed(
            text="Test tweet content #testing",
            author_id="test_user"
        )
        
        assert tweet.id is not None
        assert tweet.text == "Test tweet content #testing"
        assert tweet.author_id == "test_user"
        assert tweet.feed_type == feed.FeedType.POST
    
    def test_entity_extraction(self):
        """Test entity extraction accuracy"""
        text = "Hello @user! Check out https://example.com #hashtag $STOCK"
        entities = feed.extract_entities(text)
        
        assert len(entities.mentions) == 1
        assert entities.mentions[0].username == "user"
        
        assert len(entities.urls) == 1
        assert "example.com" in entities.urls[0].expanded_url
        
        assert len(entities.hashtags) == 1
        assert entities.hashtags[0].tag == "hashtag"
        
        assert len(entities.cashtags) == 1
        assert entities.cashtags[0].tag == "STOCK"
    
    def test_conversation_threading(self):
        """Test reply and thread functionality"""
        manager = feed.FeedManager()
        
        # Original tweet
        original = manager.create_feed(
            text="Original tweet",
            author_id="user_1"
        )
        
        # Reply
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
        
        assert reply.conversation_id == original.id
        assert reply.in_reply_to_user_id == "user_1"
        assert len(reply.referenced_feeds) == 1
    
    def test_metrics_validation(self):
        """Test metrics validation and calculations"""
        manager = feed.FeedManager()
        
        tweet = manager.create_feed(
            text="Tweet with metrics",
            author_id="user_1"
        )
        
        # Set metrics
        tweet.public_metrics = feed.PublicMetrics(
            like_count=100,
            retweet_count=50,
            reply_count=25,
            quote_count=10,
            bookmark_count=75,
            impression_count=5000
        )
        
        # Validate metrics
        assert tweet.public_metrics.like_count == 100
        assert tweet.public_metrics.impression_count == 5000
        
        # Calculate engagement rate
        total_engagement = (
            tweet.public_metrics.like_count +
            tweet.public_metrics.retweet_count +
            tweet.public_metrics.reply_count +
            tweet.public_metrics.quote_count
        )
        
        engagement_rate = total_engagement / tweet.public_metrics.impression_count
        assert 0 <= engagement_rate <= 1
    
    def test_data_persistence(self):
        """Test saving and loading functionality"""
        manager = feed.FeedManager(storage_dir="./test_data")
        
        # Create and save tweet
        original_tweet = manager.create_feed(
            text="Test persistence",
            author_id="test_user"
        )
        
        filepath = manager.save_feed(original_tweet)
        assert filepath is not None
        
        # Load and verify
        loaded_tweet = manager.load_feed(filepath)
        assert loaded_tweet.id == original_tweet.id
        assert loaded_tweet.text == original_tweet.text
        assert loaded_tweet.author_id == original_tweet.author_id

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## 📚 Integration Examples

### Arena System Integration

```python
"""
Example integration with Arena simulation system
"""
import feed

class ArenaFeedInterface:
    """Bridge between Feed system and Arena simulation"""
    
    def __init__(self, arena_config):
        self.feed_manager = feed.FeedManager()
        self.arena_config = arena_config
    
    def create_simulation_tweet(self, agent_id: str, content: str, context: dict) -> feed.Feed:
        """Create a tweet from an Arena agent"""
        
        tweet = self.feed_manager.create_feed(
            text=content,
            author_id=agent_id,
            feed_type=context.get("tweet_type", feed.FeedType.POST)
        )
        
        # Add simulation metadata
        tweet.simulation_metadata = {
            "agent_type": context.get("agent_type"),
            "simulation_step": context.get("step"),
            "strategy": context.get("strategy"),
            "target_audience": context.get("target_audience")
        }
        
        return tweet
    
    def get_feed_for_recommendation(self, user_id: str, limit: int = 100):
        """Get feeds formatted for recommendation engine"""
        
        user_feeds = self.feed_manager.search_feeds(
            author_id=user_id,
            limit=limit
        )
        
        # Format for recommendation system
        return [
            {
                "content_id": tweet.id,
                "text": tweet.text,
                "engagement_score": self._calculate_engagement_score(tweet),
                "entities": self._extract_entity_features(tweet),
                "timestamp": tweet.created_at
            }
            for tweet in user_feeds
        ]
    
    def _calculate_engagement_score(self, tweet: feed.Feed) -> float:
        """Calculate normalized engagement score"""
        if not tweet.public_metrics.impression_count:
            return 0.0
        
        total_engagement = (
            tweet.public_metrics.like_count +
            tweet.public_metrics.retweet_count * 2 +  # Retweets weighted more
            tweet.public_metrics.reply_count * 3 +    # Replies weighted most
            tweet.public_metrics.quote_count * 2.5
        )
        
        return min(total_engagement / tweet.public_metrics.impression_count, 1.0)
    
    def _extract_entity_features(self, tweet: feed.Feed) -> dict:
        """Extract entity features for ML models"""
        if not tweet.entities:
            return {"hashtags": [], "mentions": [], "urls": 0}
        
        return {
            "hashtags": [h.tag for h in tweet.entities.hashtags],
            "mentions": [m.username for m in tweet.entities.mentions],
            "urls": len(tweet.entities.urls),
            "has_media": bool(getattr(tweet, "media", None))
        }
```

## 🤝 Contributing

### Development Guidelines

1. **Type Safety**: All new code must include complete type hints
2. **Testing**: Comprehensive test coverage for all features
3. **Documentation**: Clear docstrings and usage examples
4. **Performance**: Consider memory and CPU efficiency for large datasets
5. **Backward Compatibility**: Maintain API compatibility when possible

### Code Standards

```python
# Example of proper code style
from typing import List, Optional, Dict, Any
import feed

def create_tweet_batch(
    texts: List[str],
    author_id: str,
    tweet_type: feed.FeedType = feed.FeedType.POST
) -> List[feed.Feed]:
    """
    Create a batch of tweets with consistent formatting.
    
    Args:
        texts: List of tweet content strings
        author_id: User ID for all tweets
        tweet_type: Type of tweets to create
        
    Returns:
        List of created Feed objects
        
    Raises:
        ValidationError: If any tweet content is invalid
    """
    manager = feed.FeedManager()
    tweets = []
    
    for text in texts:
        if not text.strip():
            continue  # Skip empty tweets
            
        tweet = manager.create_feed(
            text=text,
            author_id=author_id,
            feed_type=tweet_type
        )
        tweets.append(tweet)
    
    return tweets
```

## 🗓️ Roadmap

### Current Version (v1.0)
- ✅ Core data models
- ✅ Entity extraction
- ✅ Basic CRUD operations
- ✅ JSON serialization
- ✅ Type safety

### Version 1.1 (Planned)
- 🔄 Advanced search capabilities
- 🔄 Content validation rules
- 🔄 Media attachment support
- 🔄 Performance optimizations
- 🔄 Extended metrics

### Version 1.2 (Future)
- 📅 Real-time streaming support
- 📅 Graph database integration
- 📅 Advanced analytics
- 📅 Machine learning features
- 📅 Distributed storage options

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📚 Additional Resources

- **[Detailed Usage Guide](docs/USAGE.md)** - Comprehensive usage documentation
- **[API Reference](docs/API.md)** - Complete API documentation  
- **[Example Gallery](docs/EXAMPLES.md)** - Extended usage examples
- **[Performance Guide](docs/PERFORMANCE.md)** - Optimization best practices

---

**Part of the Social Arena ecosystem** - Providing the foundational data structures for next-generation social media simulation and research.