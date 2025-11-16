# Feed Viral Simulation System

完整的社交媒体病毒传播代理仿真系统 - Complete Social Media Viral Propagation Agent Simulation System

## 概述 / Overview

Feed系统现已扩展为全功能的病毒传播仿真平台，在保持原有Twitter数据结构的基础上，增加了：

The Feed system has been extended into a full-featured viral propagation simulation platform, maintaining the original Twitter data structures while adding:

- **病毒传播模拟** / Viral Propagation Simulation
- **互动仿真** / Engagement Simulation
- **趋势建模与衰减** / Trend Modeling & Decay
- **会话管理** / Session Management
- **内容治理** / Content Governance
- **深度分析** / Advanced Analytics

## 核心特性 / Core Features

### 1. 仿真模块 / Simulation Modules

#### Viral Metrics (病毒传播指标)
- **ViralityCalculator**: 计算病毒系数、传播速度、级联深度
- **ViralPotential**: 预测内容病毒传播潜力
- **ViralCascade**: 追踪完整的病毒传播级联树

```python
from feed.simulation import ViralityCalculator, ViralContext

calculator = ViralityCalculator()

# 计算病毒系数
viral_coefficient = calculator.calculate_viral_coefficient(feed)

# 预测病毒潜力
context = ViralContext(author_follower_count=10000, trending_hashtags=["viral"])
potential = calculator.predict_viral_potential(feed, context)
```

#### Engagement Simulator (互动仿真器)
- **EngagementSimulator**: 模拟真实用户互动模式
- **TimeDynamics**: 时间衰减和活跃度建模
- **EngagementWave**: 时间序列互动波形

```python
from feed.simulation import EngagementSimulator, EngagementConfig

config = EngagementConfig(simulation_duration=72, base_engagement_rate=0.03)
simulator = EngagementSimulator(config)

# 模拟互动波
wave = simulator.simulate_engagement_wave(feed, initial_exposure=5000)
print(f"Peak engagement: {wave.peak_engagement}")
```

#### Trend Decay Model (趋势衰减模型)
- **TrendLifecycle**: 完整的趋势生命周期建模
- **TrendShock**: 趋势冲击注入
- **TrendPhase**: 5阶段生命周期（萌芽、增长、峰值、衰减、尾部）

```python
from feed.simulation import TrendDecayModel

trend_model = TrendDecayModel()

# 建模趋势生命周期
lifecycle = trend_model.model_trend_lifecycle("viral", initial_momentum=100)

# 注入趋势冲击
shock = trend_model.apply_trend_shock("breaking_news", intensity=0.9, affected_feeds=feeds)
```

#### Session Manager (会话管理器)
- **SessionManager**: 管理用户内容消费会话
- **ContentConsumption**: 内容消费追踪
- **SessionResult**: 会话结果分析

```python
from feed.simulation import SessionManager, SessionParams

manager = SessionManager()

# 创建用户会话
params = SessionParams(time_budget=30, user_interests=["tech", "ai"])
session = manager.create_user_session("user_123", params)

# 模拟内容消费
result = manager.simulate_content_consumption(session, available_feeds)
print(f"Engagement rate: {result.session.engagement_rate:.2%}")
```

### 2. Feed扩展 / Feed Extensions

#### ViralFeed (病毒传播Feed)
扩展原有Feed模型，添加病毒传播追踪：

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

# 计算病毒性评分
score = viral_feed.calculate_virality_score()
is_viral = viral_feed.is_viral(threshold=0.7)
```

#### SponsoredFeed (赞助内容Feed)
支持赞助内容和广告活动追踪：

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

# 更新性能指标
sponsored_feed.update_performance_metrics(impressions=50000, clicks=2500)
roi = sponsored_feed.get_roi_metrics()
```

### 3. 治理模块 / Governance Modules

#### Safety Filter (安全过滤器)
- 毒性检测 / Toxicity detection
- 错误信息检测 / Misinformation detection
- 有害内容检测 / Harmful content detection

```python
from feed.governance import SafetyFilter, SafetyConfig

safety = SafetyFilter(SafetyConfig(toxicity_threshold=0.7))

# 评估内容安全
assessment = safety.assess_content_safety(feed)
print(f"Safety score: {assessment.overall_safety_score:.2f}")

# 过滤不安全内容
safe_feeds = safety.filter_unsafe_content(feeds, safety_threshold=0.7)
```

#### Fairness Monitor (公平性监控)
- 人口统计学公平性 / Demographic fairness
- 偏见检测 / Bias detection
- 公平性报告 / Fairness reporting

```python
from feed.governance import FairnessMonitor

monitor = FairnessMonitor()

# 监控公平性
report = monitor.monitor_demographic_fairness(recommendations, demographics)
print(f"Fairness score: {report.overall_fairness_score:.2f}")

# 检测偏见
biases = monitor.detect_bias_in_recommendations(recommendations)
```

#### Brand Safety (品牌安全)
- 关键词过滤 / Keyword filtering
- 上下文分析 / Context analysis
- 受众匹配 / Audience matching

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

### 4. 分析模块 / Analytics Modules

#### Virality Analyzer (病毒性分析器)
- 病毒内容模式分析 / Viral content pattern analysis
- 病毒性因素识别 / Virality factor identification

```python
from feed.analytics import ViralityAnalyzer

analyzer = ViralityAnalyzer()

# 分析病毒模式
patterns = analyzer.analyze_viral_content_patterns(viral_feeds)
print(f"Common hashtags: {patterns.common_hashtags}")

# 识别病毒因素
factors = analyzer.identify_virality_factors(feed)
```

#### Influence Tracker (影响力追踪器)
- 影响力演化追踪 / Influence evolution tracking
- 影响力网络分析 / Influence network analysis
- 影响力放大器识别 / Amplifier identification

```python
from feed.analytics import InfluenceTracker

tracker = InfluenceTracker()

# 追踪用户影响力
evolution = tracker.track_user_influence_evolution(user_id, user_content)
print(f"Trend: {evolution.trend}")

# 分析影响力网络
network = tracker.analyze_influence_network(root_feed, related_feeds)
```

### 5. 统一API / Unified API

**FeedSimulationAPI** 提供所有功能的高级接口：

```python
from feed import FeedSimulationAPI

# 初始化API
api = FeedSimulationAPI(storage_dir="./feeds", trace_dir="./trace")

# 创建病毒Feed
viral_feed = await api.create_viral_feed(
    text="Amazing content!",
    author_id="user_001",
    viral_coefficient=1.5
)

# 注入趋势冲击
shock = await api.inject_trend_shock("trending_topic", intensity=0.8)

# 获取病毒内容
viral_content = await api.get_viral_content(virality_threshold=0.7)

# 模拟内容生命周期
lifecycle = await api.simulate_content_lifecycle(
    feed_id="12345",
    simulation_duration=timedelta(hours=72)
)

# 应用治理过滤
filtered = await api.apply_governance_filters(feeds, filter_config)

# 分析病毒模式
patterns = await api.analyze_viral_patterns()

# 追踪用户影响力
influence = await api.track_user_influence(user_id="user_001")
```

## Trace日志系统 / Trace Logging System

所有模块使用文件化的trace日志系统，**不使用console logs**，确保可调试性：

All modules use file-based trace logging with **NO console logs** to ensure debuggability:

```
trace/
├── errors/           # 错误和异常详细记录
├── warnings/         # 警告信息
├── info/             # 信息日志
├── debug/            # 调试日志
└── performance/      # 性能指标
```

每个日志包含：
- 完整的堆栈追踪 / Complete stack traces
- 结构化数据 / Structured data
- 时间戳 / Timestamps
- 上下文信息 / Context information

## 使用示例 / Usage Examples

### 完整仿真流程 / Complete Simulation Flow

```python
import asyncio
from feed import FeedSimulationAPI, GovernanceFilterConfig
from feed.governance.brand_safety import BrandContext
from datetime import timedelta

async def run_simulation():
    # 1. 初始化
    api = FeedSimulationAPI()

    # 2. 创建内容
    viral_feed = await api.create_viral_feed(
        text="Breaking news! #viral #trending",
        author_id="user_001"
    )

    # 3. 注入趋势
    await api.inject_trend_shock("viral", intensity=0.9)

    # 4. 模拟生命周期
    lifecycle = await api.simulate_content_lifecycle(
        feed_id=viral_feed['id'],
        simulation_duration=timedelta(hours=72),
        initial_exposure=10000
    )

    # 5. 应用治理
    brand_context = BrandContext(brand_name="SafeBrand")
    filter_config = GovernanceFilterConfig(
        enable_safety_filter=True,
        brand_context=brand_context
    )

    viral_content = await api.get_viral_content(apply_governance=True)

    # 6. 分析结果
    patterns = await api.analyze_viral_patterns()
    influence = await api.track_user_influence("user_001")

    return {
        "lifecycle": lifecycle,
        "patterns": patterns,
        "influence": influence
    }

# 运行仿真
results = asyncio.run(run_simulation())
```

查看 `examples/viral_simulation_example.py` 获取完整示例。

## 架构设计 / Architecture Design

```
Feed System v2.0
├── Core Data Structures (原有)
│   ├── Feed, User, Entities, Metrics
│   └── FeedManager
│
├── Simulation Layer (新增)
│   ├── Viral Metrics
│   ├── Engagement Simulator
│   ├── Trend Decay Model
│   └── Session Manager
│
├── Feed Extensions (新增)
│   ├── ViralFeed
│   └── SponsoredFeed
│
├── Governance Layer (新增)
│   ├── Safety Filter
│   ├── Fairness Monitor
│   └── Brand Safety
│
├── Analytics Layer (新增)
│   ├── Virality Analyzer
│   └── Influence Tracker
│
└── API Layer (新增)
    ├── FeedSimulationAPI
    └── SimulationFeedManager
```

## 向后兼容性 / Backward Compatibility

✅ 完全向后兼容原有Feed系统
✅ 所有原有功能保持不变
✅ 通过继承和组合扩展，不破坏现有代码

## 性能优化 / Performance Optimization

- 大规模Feed数据的高效处理
- 实时仿真计算优化
- 内存使用优化
- 批量处理支持

## 文档 / Documentation

- **API文档**: 查看各模块的docstrings
- **示例代码**: `examples/viral_simulation_example.py`
- **Trace日志**: `trace/` 目录中的详细运行时日志
- **类型提示**: 完整的类型标注支持IDE智能提示

## 调试流程 / Debugging Process

1. 复现问题
2. 查看 `trace/` 目录中相应日期的日志
3. 检查 `trace/errors/` 中的错误JSON文件
4. 查看性能日志定位时间问题
5. 结合报告的问题与trace日志定位根因

**所有日志存储在文件中，便于事后调试分析。**

## 集成指南 / Integration Guide

### 与Arena系统集成
```python
from feed import FeedSimulationAPI

class ArenaIntegration:
    def __init__(self):
        self.feed_api = FeedSimulationAPI()

    async def simulate_viral_event(self, event_data):
        # 注入趋势冲击
        shock = await self.feed_api.inject_trend_shock(
            event_data['trend'],
            event_data['intensity']
        )
        return shock
```

### 与Agent系统集成
```python
class AgentIntegration:
    def __init__(self):
        self.feed_api = FeedSimulationAPI()

    async def agent_create_content(self, agent_id, content):
        # Agent创建病毒内容
        viral_feed = await self.feed_api.create_viral_feed(
            text=content,
            author_id=agent_id
        )
        return viral_feed
```

## 技术栈 / Tech Stack

- Python 3.8+
- Dataclasses for data modeling
- Asyncio for async operations
- Type hints for better IDE support
- File-based logging system

## 贡献 / Contributing

扩展系统时请遵循：
1. 保持向后兼容
2. 使用TraceLogger记录日志
3. 添加完整的类型提示
4. 编写单元测试
5. 更新文档

## License

Same as Feed library license.

---

**Version**: 2.0.0
**Status**: Production Ready
**Trace Logging**: Enabled (File-based, NO console logs)
