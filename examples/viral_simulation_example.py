"""
Viral Simulation Example - Comprehensive demonstration of Feed simulation capabilities

This example demonstrates:
1. Creating viral and sponsored feeds
2. Simulating engagement and trends
3. Applying governance filters
4. Analyzing viral patterns
5. Tracking influence
"""

import asyncio
from datetime import timedelta
from feed import FeedSimulationAPI, GovernanceFilterConfig
from feed.governance.brand_safety import BrandContext


async def main():
    """Main simulation example"""

    print("=" * 80)
    print("Feed Viral Simulation System - Example Usage")
    print("=" * 80)
    print()

    # Initialize API
    print("1. Initializing Feed Simulation API...")
    api = FeedSimulationAPI(
        storage_dir="./feeds",
        trace_dir="./trace"
    )
    print("✓ API initialized")
    print()

    # Create viral feed
    print("2. Creating viral feed...")
    viral_result = await api.create_viral_feed(
        text="Breaking: Amazing discovery that will change everything! #viral #trending #breakthrough",
        author_id="user_001",
        viral_coefficient=1.5,
        trend_tags=["viral", "trending", "breakthrough"]
    )
    print(f"✓ Viral feed created: {viral_result.get('id')}")
    print(f"  Virality score: {viral_result.get('virality_score', 0):.3f}")
    print()

    # Create sponsored campaign
    print("3. Creating sponsored campaign...")
    sponsored_result = await api.create_sponsored_campaign(
        text="Check out our amazing new product! Limited time offer. #sponsored",
        author_id="brand_001",
        sponsor_brand="TechCorp",
        campaign_id="campaign_2024_001",
        budget=10000.0,
        target_ctr=0.05
    )
    print(f"✓ Sponsored campaign created: {sponsored_result.get('id')}")
    print(f"  Campaign status: {sponsored_result.get('campaign_status')}")
    print()

    # Inject trend shock
    print("4. Injecting trend shock...")
    shock_result = await api.inject_trend_shock(
        trend_name="viral",
        intensity=0.8,
        duration_hours=12.0
    )
    print(f"✓ Trend shock injected: {shock_result.get('trend')}")
    print(f"  Intensity: {shock_result.get('intensity')}")
    print(f"  Momentum boost: {shock_result.get('momentum_boost', 0):.1f}")
    print()

    # Get viral content
    print("5. Retrieving viral content...")
    viral_content = await api.get_viral_content(
        virality_threshold=0.5,
        limit=10,
        apply_governance=True
    )
    print(f"✓ Found {len(viral_content)} viral feeds")
    for i, feed in enumerate(viral_content[:3], 1):
        print(f"  {i}. {feed.get('id')}: {feed.get('text', '')[:60]}...")
    print()

    # Simulate content lifecycle
    if viral_result.get('id'):
        print("6. Simulating content lifecycle...")
        lifecycle = await api.simulate_content_lifecycle(
            feed_id=viral_result['id'],
            simulation_duration=timedelta(hours=72),
            initial_exposure=5000
        )
        print(f"✓ Lifecycle simulation completed")
        if 'engagement_wave' in lifecycle:
            wave = lifecycle['engagement_wave']
            print(f"  Total engagement: {wave.get('total_engagement', 0)}")
            print(f"  Peak engagement: {wave.get('peak_engagement', 0)}")
            print(f"  Total exposure: {wave.get('total_exposure', 0)}")
        print()

    # Apply governance filters
    print("7. Applying governance filters...")
    from feed.models.feed import Feed

    # Create brand context
    brand_context = BrandContext(
        brand_name="SafeBrand",
        brand_values=["safety", "quality", "trust"],
        excluded_topics=["violence", "controversy"]
    )

    filter_config = GovernanceFilterConfig(
        enable_safety_filter=True,
        enable_brand_safety=True,
        safety_threshold=0.7,
        brand_context=brand_context
    )

    # In real usage, you would load feeds and filter them
    print(f"✓ Governance filters configured")
    print(f"  Safety filter: {filter_config.enable_safety_filter}")
    print(f"  Brand safety: {filter_config.enable_brand_safety}")
    print()

    # Analyze viral patterns
    print("8. Analyzing viral patterns...")
    patterns = await api.analyze_viral_patterns(min_virality_score=0.5)
    if 'error' not in patterns:
        print(f"✓ Viral pattern analysis completed")
        if 'common_hashtags' in patterns:
            print(f"  Top hashtags: {patterns['common_hashtags'][:3]}")
        if 'content_patterns' in patterns:
            print(f"  Content patterns: {patterns['content_patterns']}")
    print()

    # Track user influence
    print("9. Tracking user influence...")
    influence = await api.track_user_influence(
        user_id="user_001",
        time_window_days=30
    )
    if 'error' not in influence:
        print(f"✓ Influence tracking completed")
        print(f"  Peak influence: {influence.get('peak_influence', 0):.3f}")
        print(f"  Current influence: {influence.get('current_influence', 0):.3f}")
        print(f"  Trend: {influence.get('trend', 'unknown')}")
    print()

    # Get simulation status
    print("10. Getting simulation status...")
    status = await api.get_simulation_status()
    if 'error' not in status:
        print(f"✓ Simulation status:")
        print(f"  Total feeds: {status.get('total_feeds', 0)}")
        print(f"  Active trends: {status.get('active_trends', 0)}")
        print(f"  Active sessions: {status.get('active_sessions', 0)}")
    print()

    print("=" * 80)
    print("Simulation Example Completed!")
    print("=" * 80)
    print()
    print("Check the './trace' directory for detailed logs.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
