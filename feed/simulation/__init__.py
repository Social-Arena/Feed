"""
Simulation Module - Viral propagation and engagement simulation
"""

from .viral_metrics import (
    ViralityMetrics,
    ViralityCalculator,
    ViralPotential,
    ViralContext,
    ViralCascade,
    EngagementEvent
)

from .engagement_simulator import (
    EngagementSimulator,
    EngagementConfig,
    EngagementWave,
    TimeStepEngagement,
    UserBehaviorModel,
    UserSession,
    SessionEngagement,
    TimeDynamics
)

from .trend_decay_model import (
    TrendDecayModel,
    TrendConfig,
    TrendLifecycle,
    TrendPhase,
    TrendPhaseData,
    TrendShock
)

from .session_manager import (
    SessionManager,
    SessionConfig,
    SessionParams,
    SessionResult,
    ContentConsumption,
    ViewDecision
)

__all__ = [
    # Viral metrics
    'ViralityMetrics',
    'ViralityCalculator',
    'ViralPotential',
    'ViralContext',
    'ViralCascade',
    'EngagementEvent',
    # Engagement simulation
    'EngagementSimulator',
    'EngagementConfig',
    'EngagementWave',
    'TimeStepEngagement',
    'UserBehaviorModel',
    'UserSession',
    'SessionEngagement',
    'TimeDynamics',
    # Trend decay
    'TrendDecayModel',
    'TrendConfig',
    'TrendLifecycle',
    'TrendPhase',
    'TrendPhaseData',
    'TrendShock',
    # Session management
    'SessionManager',
    'SessionConfig',
    'SessionParams',
    'SessionResult',
    'ContentConsumption',
    'ViewDecision'
]
