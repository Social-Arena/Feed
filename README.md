# Feed - Twitter Simulation Framework

A comprehensive, modular Python package for Twitter data modeling and realistic simulation. Zero dependencies, pure Python implementation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🐦 **Twitter-Focused**: Designed specifically for Twitter/X data modeling
- 📊 **Realistic Simulation**: Generate authentic-looking Twitter activity with user behavior patterns
- 🏗️ **Modular Architecture**: Clean separation of models, utilities, and simulation logic
- 🚀 **Zero Dependencies**: Uses only Python standard library
- 📈 **Rich Analytics**: Track engagement, virality, and user behavior patterns
- 🔧 **Easy to Use**: Simple API with convenience functions

## Installation

### From Source

```bash
git clone https://github.com/yourusername/feed.git
cd feed
pip install -e .
```

### As a Package

```bash
pip install twitter-feed-simulator
```

## Quick Start

### Create a Simple Tweet

```python
import feed

# Create a tweet
tweet = feed.create_tweet(
    text="Hello Twitter! #Python #AI",
    author_id="user_123"
)

print(f"Created tweet: {tweet.text}")
```

### Run a Twitter Simulation

```python
import feed

# Quick simulation
tweets, stats = feed.simulate_twitter(num_tweets=100, num_users=50)

print(f"Generated {stats['total_tweets']} tweets")
print(f"Total engagement: {stats['total_engagement']:,}")
```

### Advanced Simulation

```python
import feed

# Custom configuration
config = feed.SimulationConfig(
    num_users=200,
    num_tweets=1000,
    duration_hours=24,
    like_rate=0.20,
    retweet_rate=0.05,
)

simulator = feed.TwitterSimulator(config)
tweets, stats = simulator.simulate()

# Save results
simulator.save_results()
```

## Package Structure

```
feed/
├── models/              # Data models
│   ├── feed.py         # Core Feed entity
│   ├── entities.py     # Hashtags, mentions, URLs
│   ├── metrics.py      # Engagement metrics
│   ├── references.py   # Tweet references
│   └── user.py         # User model
├── utils/              # Utilities
│   ├── manager.py      # FeedManager for CRUD
│   ├── entities.py     # Entity extraction
│   └── generators.py   # ID and data generation
└── simulation/         # Simulation engine
    ├── simulator.py    # Main orchestrator
    ├── config.py       # Configuration
    ├── behavior.py     # User behavior modeling
    ├── content.py      # Content generation
    └── engagement.py   # Engagement calculation
```

## Core Components

### Feed Model

The main data structure representing a tweet:

```python
from feed import Feed, FeedType

tweet = Feed(
    id="123456789",
    text="Hello World! #Python",
    author_id="user_1",
    feed_type=FeedType.POST,
    # ... more fields
)
```

### FeedManager

Manage tweet creation, saving, and loading:

```python
from feed import FeedManager

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

### TwitterSimulator

Simulate realistic Twitter activity:

```python
from feed import TwitterSimulator, SimulationConfig

config = SimulationConfig(
    num_users=100,
    num_tweets=500,
    duration_hours=24
)

simulator = TwitterSimulator(config)
tweets, stats = simulator.simulate()
```

## Examples

Check out the `examples/` directory for more:

- `basic_usage.py` - Basic operations and tweet creation
- `simulation_demo.py` - Various simulation scenarios

Run examples:

```bash
python examples/basic_usage.py
python examples/simulation_demo.py
```

## Features in Detail

### User Behavior Modeling

Four activity levels:
- **Influencer** (2%): 10K-1M followers, posts 2-5 times/hour
- **High** (15%): 500-10K followers, posts 0.8-2 times/hour
- **Medium** (50%): 50-500 followers, posts 0.3-0.8 times/hour
- **Low** (33%): 10-100 followers, posts 0.1-0.3 times/hour

### Content Generation

Realistic content across topics:
- Technology
- News
- Lifestyle
- Entertainment
- Sports

With automatic hashtags, mentions, and URLs.

### Engagement Simulation

Realistic metrics based on:
- Author influence
- Time decay
- Content characteristics
- Viral growth patterns (5% chance)

## Testing

Run the test suite:

```bash
python tests/test_feed.py
```

Or with pytest:

```bash
pip install pytest
pytest tests/
```

## API Reference

### Main Functions

- `create_tweet(text, author_id, **kwargs)` - Create a single tweet
- `simulate_twitter(num_tweets, num_users)` - Quick simulation
- `extract_entities(text)` - Extract hashtags, mentions, URLs

### Classes

- `Feed` - Main tweet data structure
- `FeedManager` - Tweet CRUD operations
- `TwitterSimulator` - Simulation orchestrator
- `SimulationConfig` - Simulation parameters
- `UserBehavior` - User behavior modeling
- `ContentGenerator` - Content creation
- `EngagementCalculator` - Metrics calculation

## Data Format

Tweets are saved as JSON following Twitter API v2 structure:

```json
{
  "id": "123456789",
  "text": "Hello World! #Python",
  "author_id": "user_1",
  "created_at": "2025-11-06T12:00:00.000Z",
  "entities": {
    "hashtags": [{"start": 13, "end": 20, "tag": "Python"}]
  },
  "public_metrics": {
    "like_count": 42,
    "retweet_count": 5,
    "reply_count": 3
  }
}
```

## Use Cases

- 🧪 **Testing**: Generate test data for Twitter applications
- 📊 **Research**: Analyze Twitter behavior patterns
- 🎓 **Education**: Learn about social media data structures
- 🤖 **ML Training**: Create training data for NLP models
- 📈 **Analytics**: Test analytics systems with realistic data

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Documentation

For detailed documentation, see:
- [docs/USAGE.md](docs/USAGE.md) - Comprehensive usage guide
- [examples/](examples/) - Code examples

## Requirements

- Python 3.8 or higher
- No external dependencies!

## Roadmap

- [ ] Add more platform support (Instagram, TikTok)
- [ ] Graph-based follower network modeling
- [ ] Time-series analytics export
- [ ] Real Twitter API integration
- [ ] Advanced NLP for content generation

---

**Built with ❤️ for the Twitter simulation community**
