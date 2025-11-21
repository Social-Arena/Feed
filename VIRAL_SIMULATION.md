# Feed Viral Simulation System

**Complete Social Media Viral Propagation Agent Simulation System**

## Overview

The Feed system has been extended into a full-featured viral propagation simulation platform, maintaining the original Twitter data structures while adding:

- **Viral Propagation Simulation**
- **Engagement Simulation**
- **Trend Modeling & Decay**
- **Session Management**
- **Content Governance**
- **Advanced Analytics**

## Core Features

### 1. Simulation Modules

#### Viral Metrics

- **ViralityCalculator**: Calculate viral coefficient, spread velocity, cascade depth
- **ViralPotential**: Predict content viral propagation potential
- **ViralCascade**: Track complete viral propagation cascade tree

```python
from feed.simulation import ViralityCalculator, ViralContext

calculator = ViralityCalculator()

# Calculate viral coefficient
viral_coefficient = calculator.calculate_viral_coefficient(feed)

# Predict viral potential
context = ViralContext(author_follower_count=10000, trending_hashtags=["viral"])
potential = calculator.predict_viral_potential(feed, context)
```

#### Engagement Simulator

- **EngagementSimulator**: Simulate realistic user interaction patterns
- **TimeDynamics**: Time decay and activity modeling
- **EngagementWave**: Time-series interaction waveform

```python
from feed.simulation import EngagementSimulator, EngagementConfig

config = EngagementConfig(simulation_duration=72, base_engagement_rate=0.03)
simulator = EngagementSimulator(config)

# Simulate engagement wave
wave = simulator.simulate_engagement_wave(feed, initial_exposure=5000)
print(f"Peak engagement: {wave.peak_engagement}")
```

#### Trend Decay Model

- **TrendLifecycle**: Complete trend lifecycle modeling
- **TrendShock**: Trend shock injection
- **TrendPhase**: 5-phase lifecycle (Emerging, Growth, Peak, Decline, Tail)

```python
from feed.simulation import TrendDecayModel

trend_model = TrendDecayModel()

# Model trend lifecycle
lifecycle = trend_model.model_trend_lifecycle("viral", initial_momentum=100)

# Inject trend shock
shock = trend_model.apply_trend_shock("breaking_news", intensity=0.9, affected_feeds=feeds)
```

#### Session Manager

- **SessionManager**: Manage user content consumption sessions
- **ContentConsumption**: Content consumption tracking
- **SessionResult**: Session result analysis

```python
from feed.simulation import SessionManager, SessionParams

manager = SessionManager()

# Create user session
params = SessionParams(time_budget=30, user_interests=["tech", "ai"])
session = manager.create_user_session("user_123", params)

# Simulate content consumption
result = manager.simulate_content_consumption(session, available_feeds)
print(f"Engagement rate: {result.session.engagement_rate:.2%}")
```

### 2. Feed Extensions

#### ViralFeed

Extends original Feed model with viral propagation tracking:

```python
from feed import ViralFeed

viral_feed = ViralFeed(
    id="12345",
    text="Amazing viral content!",
    author_id="user_001",
    viral_coefficient=1.8,
    spread_velocity=120.5,
    cascade_depth=5,
    viral_triggers=["emotional", "trending"]
)

# Calculate virality score
score = viral_feed.calculate_virality_score()
is_viral = viral_feed.is_viral(threshold=0.7)
```

#### SponsoredFeed

Supports sponsored content and advertising campaign tracking:

```python
from feed import SponsoredFeed

sponsored_feed = SponsoredFeed(
    id="ad_001",
    text="Check out our product!",
    author_id="brand_001",
    sponsor_brand="TechCorp",
    campaign_id="campaign_2024_q1",
    budget_allocated=10000.0,
    ctr_target=0.05
)

# Update performance metrics
sponsored_feed.update_performance_metrics(impressions=50000, clicks=2500)
roi = sponsored_feed.get_roi_metrics()
```

### 3. Governance Modules

#### Safety Filter

- Toxicity detection
- Misinformation detection
- Harmful content detection

```python
from feed.governance import SafetyFilter, SafetyConfig

safety = SafetyFilter(SafetyConfig(toxicity_threshold=0.7))

# Assess content safety
assessment = safety.assess_content_safety(feed)
print(f"Safety score: {assessment.overall_safety_score:.2f}")

# Filter unsafe content
safe_feeds = safety.filter_unsafe_content(feeds, safety_threshold=0.7)
```

#### Fairness Monitor

- Demographic fairness
- Bias detection
- Fairness reporting

```python
from feed.governance import FairnessMonitor

monitor = FairnessMonitor()

# Monitor fairness
report = monitor.monitor_demographic_fairness(recommendations, demographics)
print(f"Fairness score: {report.overall_fairness_score:.2f}")

# Detect bias
biases = monitor.detect_bias_in_recommendations(recommendations)
```

#### Brand Safety

- Keyword filtering
- Context analysis
- Audience matching

```python
from feed.governance import BrandSafety, BrandContext

brand_context = BrandContext(
    brand_name="SafeBrand",
    brand_values=["quality", "trust"],
    excluded_topics=["violence", "controversy"]
)

brand_safety = BrandSafety()
assessment = brand_safety.assess_brand_safety(feed, brand_context)
```

### 4. Analytics Modules

#### Virality Analyzer

- Viral content pattern analysis
- Virality factor identification

```python
from feed.analytics import ViralityAnalyzer

analyzer = ViralityAnalyzer()

# Analyze viral patterns
patterns = analyzer.analyze_viral_content_patterns(viral_feeds)
print(f"Common hashtags: {patterns.common_hashtags}")

# Identify virality factors
factors = analyzer.identify_virality_factors(feed)
```

#### Influence Tracker

- Influence evolution tracking
- Influence network analysis
- Amplifier identification

```python
from feed.analytics import InfluenceTracker

tracker = InfluenceTracker()

# Track user influence
evolution = tracker.track_user_influence_evolution(user_id, user_content)
print(f"Trend: {evolution.trend}")

# Analyze influence network
network = tracker.analyze_influence_network(root_feed, related_feeds)
```

### 5. Unified API

**FeedSimulationAPI** provides high-level interface for all features:

```python
from feed import FeedSimulationAPI

# Initialize API
api = FeedSimulationAPI(storage_dir="./feeds", trace_dir="./trace")

# Create viral feed
viral_feed = await api.create_viral_feed(
    text="Amazing content!",
    author_id="user_001",
    viral_coefficient=1.5
)

# Inject trend shock
shock = await api.inject_trend_shock("trending_topic", intensity=0.8)

# Get viral content
viral_content = await api.get_viral_content(virality_threshold=0.7)

# Simulate content lifecycle
lifecycle = await api.simulate_content_lifecycle(
    feed_id="12345",
    simulation_duration=timedelta(hours=72)
)

# Apply governance filters
filtered = await api.apply_governance_filters(feeds, filter_config)

# Analyze viral patterns
patterns = await api.analyze_viral_patterns()

# Track user influence
influence = await api.track_user_influence(user_id="user_001")
```

## Trace Logging System

All modules use file-based trace logging with **NO console logs** to ensure debuggability:

```
trace/
├── errors/           # Detailed error and exception logs
├── warnings/         # Warning information
├── info/             # Information logs
├── debug/            # Debug logs
└── performance/      # Performance metrics
```

Each log contains:
- Complete stack traces
- Structured data
- Timestamps
- Context information

## Usage Examples

### Complete Simulation Flow

```python
import asyncio
from feed import FeedSimulationAPI, GovernanceFilterConfig
from feed.governance.brand_safety import BrandContext
from datetime import timedelta

async def run_simulation():
    # 1. Initialize
    api = FeedSimulationAPI()

    # 2. Create content
    viral_feed = await api.create_viral_feed(
        text="Breaking news! #viral #trending",
        author_id="user_001"
    )

    # 3. Inject trend
    await api.inject_trend_shock("viral", intensity=0.9)

    # 4. Simulate lifecycle
    lifecycle = await api.simulate_content_lifecycle(
        feed_id=viral_feed['id'],
        simulation_duration=timedelta(hours=72),
        initial_exposure=10000
    )

    # 5. Apply governance
    brand_context = BrandContext(brand_name="SafeBrand")
    filter_config = GovernanceFilterConfig(
        enable_safety_filter=True,
        brand_context=brand_context
    )

    viral_content = await api.get_viral_content(apply_governance=True)

    # 6. Analyze results
    patterns = await api.analyze_viral_patterns()
    influence = await api.track_user_influence("user_001")

    return {
        "lifecycle": lifecycle,
        "patterns": patterns,
        "influence": influence
    }

# Run simulation
results = asyncio.run(run_simulation())
```

See `examples/viral_simulation_example.py` for complete example.

## Architecture Design

```
Feed System v2.0
├── Core Data Structures (Original)
│   ├── Feed, User, Entities, Metrics
│   └── FeedManager
│
├── Simulation Layer (New)
│   ├── Viral Metrics
│   ├── Engagement Simulator
│   ├── Trend Decay Model
│   └── Session Manager
│
├── Feed Extensions (New)
│   ├── ViralFeed
│   └── SponsoredFeed
│
├── Governance Layer (New)
│   ├── Safety Filter
│   ├── Fairness Monitor
│   └── Brand Safety
│
├── Analytics Layer (New)
│   ├── Virality Analyzer
│   └── Influence Tracker
│
└── API Layer (New)
    ├── FeedSimulationAPI
    └── SimulationFeedManager
```

## Backward Compatibility

✅ Fully backward compatible with original Feed system  
✅ All original functionality preserved  
✅ Extended through inheritance and composition, no breaking changes  

## Performance Optimization

- Efficient processing of large-scale Feed data
- Real-time simulation computation optimization
- Memory usage optimization
- Batch processing support

## Documentation

- **API Documentation**: See module docstrings
- **Example Code**: `examples/viral_simulation_example.py`
- **Trace Logs**: Detailed runtime logs in `trace/` directory
- **Type Hints**: Complete type annotations for IDE support

## Debugging Process

1. Reproduce the issue
2. Check `trace/` directory for relevant logs
3. Check `trace/errors/` for error JSON files
4. Review performance logs to locate timing issues
5. Combine reported issues with trace logs to identify root cause

**All logs stored in files for post-mortem debugging.**

## Integration Guide

### Integration with Arena System

```python
from feed import FeedSimulationAPI

class ArenaIntegration:
    def __init__(self):
        self.feed_api = FeedSimulationAPI()

    async def simulate_viral_event(self, event_data):
        # Inject trend shock
        shock = await self.feed_api.inject_trend_shock(
            event_data['trend'],
            event_data['intensity']
        )
        return shock
```

### Integration with Agent System

```python
class AgentIntegration:
    def __init__(self):
        self.feed_api = FeedSimulationAPI()

    async def agent_create_content(self, agent_id, content):
        # Agent creates viral content
        viral_feed = await self.feed_api.create_viral_feed(
            text=content,
            author_id=agent_id
        )
        return viral_feed
```

## Tech Stack

- Python 3.8+
- Dataclasses for data modeling
- Asyncio for async operations
- Type hints for better IDE support
- File-based logging system

## Contributing

When extending the system, please follow:
1. Maintain backward compatibility
2. Use TraceLogger for logging
3. Add complete type hints
4. Write unit tests
5. Update documentation

## License

Same as Feed library license.

---

**Version**: 2.0.0  
**Status**: Production Ready  
**Trace Logging**: Enabled (File-based, NO console logs)
