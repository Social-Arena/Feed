# Feed System Architecture

**Software Engineering Architecture Documentation**

This document provides comprehensive Mermaid diagrams representing the Feed system architecture from multiple perspectives.

---

## 1. System Overview - Layered Architecture

```mermaid
graph TB
    subgraph "External Integrations"
        Arena[Arena System]
        Agent[Agent System]
        External[External Applications]
    end

    subgraph "API Layer"
        API[FeedSimulationAPI]
        Config[GovernanceFilterConfig]
    end

    subgraph "Extension Layer"
        ViralFeed[ViralFeed Extension]
        SponsoredFeed[SponsoredFeed Extension]
    end

    subgraph "Core Layer"
        Models[Core Models]
        FeedManager[FeedManager]
        Utils[Utilities]
    end

    subgraph "Simulation Layer"
        ViralMetrics[Viral Metrics]
        Engagement[Engagement Simulator]
        Trend[Trend Decay Model]
        Session[Session Manager]
    end

    subgraph "Governance Layer"
        Safety[Safety Filter]
        Fairness[Fairness Monitor]
        Brand[Brand Safety]
    end

    subgraph "Analytics Layer"
        ViralityAnalyzer[Virality Analyzer]
        InfluenceTracker[Influence Tracker]
    end

    subgraph "Infrastructure"
        Storage[(JSON Storage)]
        Trace[Trace Logger]
    end

    Arena --> API
    Agent --> API
    External --> API

    API --> Extension Layer
    API --> Simulation Layer
    API --> Governance Layer
    API --> Analytics Layer

    Extension Layer --> Core Layer
    Simulation Layer --> Core Layer
    Governance Layer --> Core Layer
    Analytics Layer --> Core Layer

    Core Layer --> Infrastructure
    API --> Infrastructure

    style API fill:#e1f5ff
    style Core Layer fill:#fff4e1
    style Simulation Layer fill:#ffe1f0
    style Governance Layer fill:#e1ffe8
    style Analytics Layer fill:#f0e1ff
```

---

## 2. Core Data Models - Entity Relationship

```mermaid
classDiagram
    class Feed {
        +string id
        +string text
        +string author_id
        +string created_at
        +FeedType feed_type
        +string conversation_id
        +string in_reply_to_user_id
        +List~ReferencedFeed~ referenced_feeds
        +Entities entities
        +PublicMetrics public_metrics
        +string lang
        +string source
        +bool possibly_sensitive
        +string platform
        +to_dict() Dict
        +from_dict(data) Feed
    }

    class FeedType {
        <<enumeration>>
        POST
        REPLY
        QUOTE
        RETWEET
        THREAD
    }

    class Entities {
        +List~HashtagEntity~ hashtags
        +List~MentionEntity~ mentions
        +List~UrlEntity~ urls
        +to_dict() Dict
    }

    class HashtagEntity {
        +int start
        +int end
        +string tag
    }

    class MentionEntity {
        +int start
        +int end
        +string username
        +string id
    }

    class UrlEntity {
        +int start
        +int end
        +string url
        +string expanded_url
        +string display_url
        +string title
        +string description
    }

    class PublicMetrics {
        +int retweet_count
        +int reply_count
        +int like_count
        +int quote_count
        +int bookmark_count
        +int impression_count
    }

    class ReferencedFeed {
        +string type
        +string id
    }

    class ReferencedFeedType {
        <<enumeration>>
        RETWEETED
        QUOTED
        REPLIED_TO
    }

    class User {
        +string id
        +string username
        +string name
        +string profile_image_url
        +bool verified
        +string description
        +string created_at
        +Dict public_metrics
        +string location
        +to_dict() Dict
    }

    class ViralFeed {
        +float viral_coefficient
        +float spread_velocity
        +int cascade_depth
        +int influence_reach
        +List~string~ viral_triggers
        +List~string~ propagation_path
        +List~string~ amplification_nodes
        +float trend_alignment_score
        +float trend_acceleration_factor
        +string peak_engagement_time
        +string virality_phase
        +calculate_virality_score() float
        +is_viral(threshold) bool
        +update_virality_phase()
    }

    class SponsoredFeed {
        +string sponsor_brand
        +string campaign_id
        +float budget_allocated
        +float budget_spent
        +float ctr_target
        +float actual_ctr
        +int impressions_delivered
        +int clicks_received
        +string campaign_status
        +update_performance_metrics()
        +get_roi_metrics() Dict
    }

    Feed --> FeedType
    Feed --> Entities
    Feed --> PublicMetrics
    Feed --> ReferencedFeed
    Entities --> HashtagEntity
    Entities --> MentionEntity
    Entities --> UrlEntity
    ReferencedFeed --> ReferencedFeedType
    ViralFeed --|> Feed
    SponsoredFeed --|> Feed
```

---

## 3. Component Architecture - Module Dependencies

```mermaid
graph LR
    subgraph "API Module"
        API[simulation_api.py<br/>FeedSimulationAPI<br/>GovernanceFilterConfig]
    end

    subgraph "Models Module"
        Feed[feed.py<br/>Feed, FeedType]
        Entities[entities.py<br/>Entities, HashtagEntity<br/>MentionEntity, UrlEntity]
        Metrics[metrics.py<br/>PublicMetrics]
        References[references.py<br/>ReferencedFeed<br/>ReferencedFeedType]
        User[user.py<br/>User]
    end

    subgraph "Extensions Module"
        VFeed[viral_feed.py<br/>ViralFeed]
        SFeed[sponsored_feed.py<br/>SponsoredFeed]
    end

    subgraph "Simulation Module"
        VM[viral_metrics.py<br/>ViralityCalculator<br/>ViralityMetrics<br/>ViralContext]
        ES[engagement_simulator.py<br/>EngagementSimulator<br/>EngagementWave<br/>TimeDynamics]
        TD[trend_decay_model.py<br/>TrendDecayModel<br/>TrendLifecycle<br/>TrendShock]
        SM[session_manager.py<br/>SessionManager<br/>SessionParams<br/>SessionResult]
    end

    subgraph "Governance Module"
        SF[safety_filter.py<br/>SafetyFilter<br/>SafetyAssessment<br/>ToxicityDetector]
        FM[fairness_monitor.py<br/>FairnessMonitor<br/>FairnessReport]
        BS[brand_safety.py<br/>BrandSafety<br/>BrandContext]
    end

    subgraph "Analytics Module"
        VA[virality_analyzer.py<br/>ViralityAnalyzer<br/>ViralContentPatterns]
        IT[influence_tracker.py<br/>InfluenceTracker<br/>InfluenceEvolution]
    end

    subgraph "Utils Module"
        Manager[manager.py<br/>FeedManager]
        SimMgr[simulation_manager.py<br/>SimulationFeedManager<br/>SimulationConfig]
        Generators[generators.py<br/>generate_feed_id<br/>create_sample_user]
        EntityUtils[entities.py<br/>extract_entities]
        Trace[trace_logger.py<br/>TraceLogger]
    end

    API --> VFeed
    API --> SFeed
    API --> VM
    API --> ES
    API --> TD
    API --> SM
    API --> SF
    API --> FM
    API --> BS
    API --> VA
    API --> IT
    API --> SimMgr

    VFeed --> Feed
    SFeed --> Feed
    
    Feed --> Entities
    Feed --> Metrics
    Feed --> References

    VM --> Feed
    ES --> Feed
    TD --> Feed
    SM --> Feed

    SF --> Feed
    FM --> Feed
    BS --> Feed

    VA --> Feed
    IT --> Feed

    Manager --> Feed
    SimMgr --> Manager
    SimMgr --> VM
    SimMgr --> ES
    SimMgr --> TD
    SimMgr --> SM

    EntityUtils --> Entities

    API --> Trace
    VM --> Trace
    ES --> Trace
    SF --> Trace
    VA --> Trace

    style API fill:#e1f5ff
    style Models Module fill:#fff4e1
    style Simulation Module fill:#ffe1f0
    style Governance Module fill:#e1ffe8
    style Analytics Module fill:#f0e1ff
```

---

## 4. Simulation System - Process Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FeedSimulationAPI
    participant SimMgr as SimulationFeedManager
    participant VCalc as ViralityCalculator
    participant ESim as EngagementSimulator
    participant Trend as TrendDecayModel
    participant Gov as Governance Modules
    participant Storage as JSON Storage

    Client->>API: create_viral_feed(text, author_id)
    API->>SimMgr: create_viral_feed()
    SimMgr->>VCalc: calculate_viral_coefficient()
    VCalc-->>SimMgr: viral_metrics
    SimMgr-->>API: viral_feed
    API->>Storage: save_feed()
    API-->>Client: viral_feed_dict

    Client->>API: inject_trend_shock(trend, intensity)
    API->>Trend: apply_trend_shock()
    Trend->>Trend: calculate_momentum_boost()
    Trend-->>API: shock_result
    API-->>Client: shock_dict

    Client->>API: simulate_content_lifecycle(feed_id)
    API->>Storage: load_feed(feed_id)
    Storage-->>API: feed
    API->>ESim: simulate_engagement_wave()
    ESim->>ESim: simulate_time_steps()
    ESim->>ESim: calculate_time_decay()
    ESim-->>API: engagement_wave
    API->>VCalc: calculate_complete_metrics()
    VCalc-->>API: virality_metrics
    API-->>Client: lifecycle_result

    Client->>API: apply_governance_filters(feeds)
    API->>Gov: filter_unsafe_content()
    Gov->>Gov: assess_content_safety()
    Gov->>Gov: assess_brand_safety()
    Gov-->>API: filtered_feeds
    API-->>Client: safe_feeds

    Client->>API: analyze_viral_patterns()
    API->>Storage: get_viral_content()
    Storage-->>API: viral_feeds
    API->>VA as ViralityAnalyzer: analyze_viral_content_patterns()
    VA->>VA: extract_features()
    VA->>VA: identify_trends()
    VA-->>API: patterns
    API-->>Client: pattern_dict
```

---

## 5. Engagement Simulation - Detailed Flow

```mermaid
stateDiagram-v2
    [*] --> FeedCreation
    
    state FeedCreation {
        [*] --> GenerateID
        GenerateID --> ExtractEntities
        ExtractEntities --> SetMetrics
        SetMetrics --> [*]
    }
    
    FeedCreation --> InitialExposure
    
    state SimulationLoop {
        [*] --> TimeStep
        TimeStep --> CalculateDecay
        CalculateDecay --> CalculateActivity
        CalculateActivity --> SimulateEngagement
        SimulateEngagement --> UpdateMetrics
        UpdateMetrics --> ViralPropagation
        ViralPropagation --> TimeStep: Next Step
        ViralPropagation --> [*]: Complete
    }
    
    InitialExposure --> SimulationLoop
    
    SimulationLoop --> AnalyzeResults
    
    state AnalyzeResults {
        [*] --> CalculateVirality
        CalculateVirality --> FindPeak
        FindPeak --> CalculateCascade
        CalculateCascade --> [*]
    }
    
    AnalyzeResults --> GovernanceCheck
    
    state GovernanceCheck {
        [*] --> SafetyFilter
        SafetyFilter --> ToxicityCheck
        ToxicityCheck --> MisinfoCheck
        MisinfoCheck --> BrandSafety
        BrandSafety --> [*]
    }
    
    GovernanceCheck --> [*]
```

---

## 6. Data Flow Architecture

```mermaid
flowchart TD
    Start([Client Request]) --> CreateFeed{Create Feed?}
    
    CreateFeed -->|Yes| FeedGen[Generate Feed ID]
    FeedGen --> Extract[Extract Entities]
    Extract --> Validate[Validate Data]
    Validate --> Store1[(Save to Storage)]
    
    CreateFeed -->|No| LoadFeed{Load Feed?}
    LoadFeed -->|Yes| Retrieve[(Retrieve from Storage)]
    
    Store1 --> ProcessType{Processing Type}
    Retrieve --> ProcessType
    
    ProcessType -->|Viral| CalcViral[Calculate Viral Metrics]
    CalcViral --> VC[Viral Coefficient]
    CalcViral --> SV[Spread Velocity]
    CalcViral --> CD[Cascade Depth]
    VC --> CombineViral[Combine Metrics]
    SV --> CombineViral
    CD --> CombineViral
    
    ProcessType -->|Engagement| SimEng[Simulate Engagement]
    SimEng --> TimeLoop[Time Step Loop]
    TimeLoop --> Decay[Apply Time Decay]
    Decay --> Activity[Activity Multiplier]
    Activity --> GenEng[Generate Engagements]
    GenEng --> Update[Update Exposure]
    Update --> TimeLoop
    TimeLoop --> Wave[Engagement Wave]
    
    ProcessType -->|Trend| TrendMod[Trend Modeling]
    TrendMod --> Lifecycle[Lifecycle Phases]
    Lifecycle --> Shock{Inject Shock?}
    Shock -->|Yes| ApplyShock[Apply Momentum Boost]
    Shock -->|No| Natural[Natural Decay]
    ApplyShock --> TrendResult[Trend Result]
    Natural --> TrendResult
    
    ProcessType -->|Governance| GovFilter[Governance Filters]
    GovFilter --> Safety[Safety Check]
    Safety --> Toxicity[Toxicity Detection]
    Safety --> Misinfo[Misinformation Detection]
    Safety --> Harmful[Harmful Content Detection]
    Toxicity --> SafeScore[Safety Score]
    Misinfo --> SafeScore
    Harmful --> SafeScore
    SafeScore --> BrandCheck[Brand Safety Check]
    BrandCheck --> FilterResult[Filtered Content]
    
    CombineViral --> ResultAgg[Aggregate Results]
    Wave --> ResultAgg
    TrendResult --> ResultAgg
    FilterResult --> ResultAgg
    
    ResultAgg --> Analytics{Analyze?}
    Analytics -->|Yes| Pattern[Pattern Analysis]
    Pattern --> Influence[Influence Tracking]
    Influence --> AnalyticsResult[Analytics Report]
    
    Analytics -->|No| FinalResult[Final Result]
    AnalyticsResult --> FinalResult
    
    FinalResult --> Store2[(Save Results)]
    Store2 --> Log[Trace Logger]
    Log --> End([Return to Client])
    
    style CreateFeed fill:#e1f5ff
    style CalcViral fill:#ffe1f0
    style SimEng fill:#ffe1f0
    style GovFilter fill:#e1ffe8
    style Pattern fill:#f0e1ff
```

---

## 7. Class Interaction - Simulation Core

```mermaid
classDiagram
    class FeedSimulationAPI {
        -SimulationFeedManager manager
        -SafetyFilter safety_filter
        -FairnessMonitor fairness_monitor
        -BrandSafety brand_safety
        -ViralityAnalyzer virality_analyzer
        -InfluenceTracker influence_tracker
        +inject_trend_shock(trend, intensity)
        +get_viral_content(threshold)
        +simulate_content_lifecycle(feed_id)
        +apply_governance_filters(feeds)
        +analyze_viral_patterns()
        +track_user_influence(user_id)
    }

    class SimulationFeedManager {
        -FeedManager base_manager
        -ViralityCalculator virality_calc
        -EngagementSimulator engagement_sim
        -TrendDecayModel trend_model
        -SessionManager session_manager
        +create_viral_feed(text, author_id)
        +create_sponsored_feed(text, sponsor)
        +simulate_feed_engagement(feed)
        +inject_trend_shock(trend, intensity)
        +get_viral_content(threshold)
    }

    class ViralityCalculator {
        -Dict~string,List~ engagement_history
        +calculate_viral_coefficient(feed)
        +calculate_spread_velocity(feed)
        +predict_viral_potential(feed, context)
        +track_viral_cascade(feed_id)
        +calculate_complete_metrics(feed)
    }

    class EngagementSimulator {
        -EngagementConfig config
        -Dict~string,UserBehaviorModel~ user_behaviors
        -TimeDynamics time_dynamics
        +simulate_engagement_wave(feed, exposure)
        +simulate_user_session_engagement(user, feeds)
    }

    class TimeDynamics {
        +calculate_time_decay(feed, time)
        +get_hourly_activity_multiplier(hour)
    }

    class TrendDecayModel {
        -Dict~string,TrendState~ active_trends
        +model_trend_lifecycle(trend, momentum)
        +apply_trend_shock(trend, intensity)
        +get_trend_momentum(trend)
    }

    class SessionManager {
        -Dict~string,UserSession~ active_sessions
        +create_user_session(user_id, params)
        +simulate_content_consumption(session, feeds)
        +end_session(session_id)
    }

    class SafetyFilter {
        -ToxicityDetector toxicity_detector
        -MisinformationDetector misinfo_detector
        -HarmfulContentDetector harmful_detector
        +assess_content_safety(feed)
        +filter_unsafe_content(feeds)
    }

    class ViralityAnalyzer {
        -Dict~string,List~ emotional_keywords
        +analyze_viral_content_patterns(feeds)
        +identify_virality_factors(feed)
    }

    class InfluenceTracker {
        +track_user_influence_evolution(user_id, content)
        +analyze_influence_network(root, related)
        +identify_key_amplifiers(network)
    }

    FeedSimulationAPI --> SimulationFeedManager
    FeedSimulationAPI --> SafetyFilter
    FeedSimulationAPI --> ViralityAnalyzer
    FeedSimulationAPI --> InfluenceTracker

    SimulationFeedManager --> ViralityCalculator
    SimulationFeedManager --> EngagementSimulator
    SimulationFeedManager --> TrendDecayModel
    SimulationFeedManager --> SessionManager

    EngagementSimulator --> TimeDynamics
```

---

## 8. Storage & Infrastructure

```mermaid
graph TB
    subgraph "Application Layer"
        API[FeedSimulationAPI]
        Manager[SimulationFeedManager]
    end

    subgraph "Storage Layer"
        FileManager[FeedManager]
        JSON[(JSON Files)]
        NamingConv[Naming Convention:<br/>feed-YYYYMMDD_HHMMSS-id.json]
    end

    subgraph "Trace System"
        Logger[TraceLogger]
        
        subgraph "Log Files"
            Errors[errors/]
            Warnings[warnings/]
            Info[info/]
            Debug[debug/]
            Perf[performance/]
        end
    end

    subgraph "File System"
        Feeds[./feeds/]
        Trace[./trace/]
    end

    API --> Manager
    Manager --> FileManager
    
    FileManager --> JSON
    FileManager --> NamingConv
    JSON --> Feeds
    
    API --> Logger
    Manager --> Logger
    FileManager --> Logger
    
    Logger --> Errors
    Logger --> Warnings
    Logger --> Info
    Logger --> Debug
    Logger --> Perf
    
    Errors --> Trace
    Warnings --> Trace
    Info --> Trace
    Debug --> Trace
    Perf --> Trace

    style JSON fill:#fff4e1
    style Logger fill:#e1f5ff
    style Feeds fill:#e1ffe8
    style Trace fill:#e1ffe8
```

---

## 9. Extension Pattern - Viral & Sponsored Feeds

```mermaid
classDiagram
    class Feed {
        <<base>>
        #id: string
        #text: string
        #author_id: string
        #public_metrics: PublicMetrics
        +to_dict() Dict
        +from_dict(data) Feed
    }

    class ViralFeed {
        +viral_coefficient: float
        +spread_velocity: float
        +cascade_depth: int
        +viral_triggers: List~string~
        +propagation_path: List~string~
        +virality_phase: string
        +calculate_virality_score() float
        +is_viral(threshold) bool
        +update_virality_phase()
        +add_propagation_node(user_id)
        +get_propagation_stats() Dict
    }

    class SponsoredFeed {
        +sponsor_brand: string
        +campaign_id: string
        +budget_allocated: float
        +budget_spent: float
        +ctr_target: float
        +actual_ctr: float
        +campaign_status: string
        +update_performance_metrics()
        +get_roi_metrics() Dict
        +calculate_campaign_effectiveness() float
    }

    Feed <|-- ViralFeed : extends
    Feed <|-- SponsoredFeed : extends

    note for ViralFeed "Adds viral propagation\ntracking and metrics"
    note for SponsoredFeed "Adds campaign performance\ntracking and ROI metrics"
```

---

## 10. System Integration Points

```mermaid
graph LR
    subgraph "External Systems"
        Arena[Arena System<br/>Social Simulation]
        Agent[Agent System<br/>AI Agents]
        Analytics[External Analytics<br/>Dashboard]
    end

    subgraph "Feed API Interface"
        API[FeedSimulationAPI]
        
        subgraph "API Operations"
            Create[create_viral_feed]
            Campaign[create_sponsored_campaign]
            Shock[inject_trend_shock]
            Lifecycle[simulate_content_lifecycle]
            GetViral[get_viral_content]
            Governance[apply_governance_filters]
            Analyze[analyze_viral_patterns]
            Influence[track_user_influence]
            Status[get_simulation_status]
        end
    end

    subgraph "Internal Processing"
        Sim[Simulation Engine]
        Gov[Governance Engine]
        Anly[Analytics Engine]
    end

    subgraph "Data Persistence"
        Storage[(JSON Storage)]
        Logs[Trace Logs]
    end

    Arena --> Create
    Arena --> Shock
    Arena --> GetViral
    
    Agent --> Create
    Agent --> Lifecycle
    Agent --> Influence
    
    Analytics --> Analyze
    Analytics --> Status
    
    Create --> Sim
    Campaign --> Sim
    Shock --> Sim
    Lifecycle --> Sim
    GetViral --> Sim
    
    Governance --> Gov
    
    Analyze --> Anly
    Influence --> Anly
    
    Sim --> Storage
    Gov --> Storage
    Anly --> Storage
    
    API --> Logs

    style Arena fill:#ffe1f0
    style Agent fill:#ffe1f0
    style Analytics fill:#f0e1ff
    style API fill:#e1f5ff
```

---

## Architecture Summary

### Layer Responsibilities

1. **API Layer**: External interface for system integration
2. **Extension Layer**: Specialized feed types with enhanced capabilities
3. **Core Layer**: Fundamental data structures and operations
4. **Simulation Layer**: Viral propagation and engagement modeling
5. **Governance Layer**: Content safety and compliance
6. **Analytics Layer**: Pattern analysis and insights
7. **Infrastructure Layer**: Storage and logging

### Key Design Patterns

- **Extension Pattern**: ViralFeed and SponsoredFeed extend base Feed
- **Manager Pattern**: FeedManager and SimulationFeedManager handle CRUD
- **Strategy Pattern**: Multiple detectors in SafetyFilter
- **Observer Pattern**: TraceLogger throughout system
- **Factory Pattern**: Feed creation methods
- **Facade Pattern**: FeedSimulationAPI simplifies complexity

### Data Flow

1. Client requests → API Layer
2. API Layer → Specialized modules (Simulation/Governance/Analytics)
3. Modules → Core Models
4. Core Models → Storage Layer
5. All operations → Trace Logger

### Integration Points

- **Arena System**: Trend injection, viral content retrieval
- **Agent System**: Content creation, lifecycle simulation
- **External Analytics**: Pattern analysis, influence tracking

### Technology Stack

- **Language**: Python 3.8+
- **Data Structures**: Dataclasses
- **Async Support**: Asyncio
- **Storage**: JSON files
- **Logging**: Custom file-based trace system
- **Dependencies**: Zero (standard library only)

---

*Generated: 2024*
*Version: 2.0.0*

