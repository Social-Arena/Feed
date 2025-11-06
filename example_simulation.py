#!/usr/bin/env python3
"""
Example Social Media Simulation Script
Demonstrates how to use the feed module for social simulation
"""

import sys
import os
from datetime import datetime

# Import the Feed module
# When installed: import feed
# For local development:
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Feed as feed


def run_basic_simulation():
    """Run a basic social media simulation"""
    print("\n" + "="*60)
    print("Basic Social Media Simulation")
    print("="*60)
    
    # Create a simulator with custom configuration
    config = feed.SimulationConfig(
        num_users=50,
        num_feeds=100,
        duration_hours=24,
        platform="twitter",
        like_rate=0.20,  # 20% like rate
        repost_rate=0.05,  # 5% repost rate
        with_media_rate=0.40,  # 40% of posts have media
    )
    
    simulator = feed.SocialSimulator(config)
    
    # Generate users
    print(f"\nGenerating {config.num_users} users...")
    users = simulator.generate_users()
    
    # Show user distribution
    user_types = {}
    for user in users:
        user_types[user.activity_level] = user_types.get(user.activity_level, 0) + 1
    
    print("\nUser Distribution:")
    for level, count in user_types.items():
        print(f"  {level}: {count} users")
    
    # Run simulation
    print(f"\nSimulating {config.num_feeds} feeds over {config.duration_hours} hours...")
    feeds, stats = simulator.simulate_activity()
    
    # Display statistics
    print("\n" + "-"*40)
    print("Simulation Statistics:")
    print("-"*40)
    print(f"Total Feeds: {stats['total_feeds']}")
    print(f"Total Replies: {stats['total_replies']}")
    print(f"Total Quotes: {stats['total_quotes']}")
    print(f"Total Media Posts: {stats['total_media']}")
    print(f"Total Engagement: {stats['total_engagement']:,}")
    print(f"Viral Feeds: {stats['viral_feeds']}")
    
    print(f"\nFeeds by Type:")
    for feed_type, count in stats['by_type'].items():
        print(f"  {feed_type}: {count}")
    
    print(f"\nTop 5 Active Hours:")
    sorted_hours = sorted(stats['by_hour'].items(), key=lambda x: x[1], reverse=True)[:5]
    for hour, count in sorted_hours:
        print(f"  {hour:02d}:00 - {count} feeds")
    
    # Save simulation results
    print("\n" + "-"*40)
    print("Saving simulation results...")
    result = simulator.save_simulation(
        output_dir="./simulation_output",
        save_individual=True,
        save_response=True
    )
    print(f"Saved {len(result['saved_files'])} files to {result['output_directory']}")
    
    # Show sample feed
    if feeds:
        print("\n" + "-"*40)
        print("Sample Feed from Simulation:")
        print("-"*40)
        sample_feed = feeds[len(feeds)//2]  # Get middle feed
        print(f"Author: user_{sample_feed.author_id}")
        print(f"Text: {sample_feed.text}")
        print(f"Type: {sample_feed.feed_type.value}")
        print(f"Engagement: {sample_feed.public_metrics.like_count} likes, "
              f"{sample_feed.public_metrics.repost_count} reposts")


def run_influencer_simulation():
    """Run a simulation focused on influencer behavior"""
    print("\n" + "="*60)
    print("Influencer-Focused Simulation")
    print("="*60)
    
    # Configure for influencer-heavy simulation
    config = feed.SimulationConfig(
        num_users=20,  # Fewer users but more active
        num_feeds=200,
        duration_hours=48,
        platform="instagram",
        like_rate=0.30,  # Higher engagement
        with_media_rate=0.70,  # More visual content
    )
    
    simulator = feed.SocialSimulator(config)
    
    # Manually create some influencers
    influencers = []
    for i in range(5):
        influencer = feed.UserBehavior(
            user_id=f"inf_{i}",
            username=f"influencer_{i}",
            activity_level="influencer",
            interests=["lifestyle", "entertainment"],
            posting_frequency=5.0,
            engagement_probability=0.8,
            follower_count=50000 + i * 10000,
            following_count=500,
        )
        influencers.append(influencer)
    
    # Add influencers to simulator
    simulator.users.extend(influencers)
    
    # Generate regular users
    regular_users = simulator.generate_users(15)
    
    print(f"Created {len(influencers)} influencers and {len(regular_users)} regular users")
    
    # Run simulation
    feeds, stats = simulator.simulate_activity()
    
    # Find most engaged posts
    top_feeds = sorted(feeds, key=lambda f: f.public_metrics.like_count, reverse=True)[:5]
    
    print("\nTop 5 Most Engaged Posts:")
    for i, feed in enumerate(top_feeds, 1):
        print(f"\n{i}. Author: {feed.author_id}")
        print(f"   Text: {feed.text[:100]}...")
        print(f"   Likes: {feed.public_metrics.like_count:,}")
        print(f"   Reposts: {feed.public_metrics.repost_count:,}")


def demonstrate_module_usage():
    """Demonstrate simple module usage patterns"""
    print("\n" + "="*60)
    print("Module Usage Examples")
    print("="*60)
    
    # Example 1: Create a single feed
    print("\n1. Creating a single feed:")
    my_feed = feed.create_feed(
        text="Hello from the feed module! #Python #Coding",
        author_id="demo_user"
    )
    print(f"   Created feed with ID: {my_feed.id}")
    
    # Example 2: Generate multiple feeds quickly
    print("\n2. Generating sample feeds:")
    sample_feeds = feed.generate_feeds(count=5, platform="twitter")
    print(f"   Generated {len(sample_feeds)} sample feeds")
    
    # Example 3: Create a thread
    print("\n3. Creating a thread:")
    manager = feed.FeedManager()
    thread_texts = [
        "Let's talk about social media simulation! 🧵 (1/3)",
        "The feed module makes it easy to simulate realistic social media data (2/3)",
        "Perfect for testing, research, or building social apps! (3/3)"
    ]
    thread = feed.create_thread(thread_texts, "thread_author", manager, "twitter")
    print(f"   Created thread with {len(thread)} posts")
    
    # Example 4: Extract entities
    print("\n4. Extracting entities from text:")
    text = "Check out @user123's post about #Python and #DataScience! https://example.com"
    entities = feed.extract_entities(text)
    if entities:
        print(f"   Hashtags: {[h.tag for h in entities.hashtags]}")
        print(f"   Mentions: {[m.username for m in entities.mentions]}")
        print(f"   URLs: {len(entities.urls)} found")
    
    # Example 5: Create user with metrics
    print("\n5. Creating a user:")
    user = feed.create_sample_user(
        user_id="12345",
        username="demo_user",
        name="Demo User"
    )
    print(f"   User: @{user.username} ({user.name})")
    print(f"   Followers: {user.public_metrics['followers_count']:,}")
    
    # Example 6: Save and load feeds
    print("\n6. Saving and loading feeds:")
    filepath = feed.save_feed(my_feed)
    print(f"   Saved to: {filepath}")
    loaded_feed = feed.load_feed(filepath)
    print(f"   Loaded feed text: {loaded_feed.text[:50]}...")


def run_platform_comparison():
    """Compare behavior across different platforms"""
    print("\n" + "="*60)
    print("Cross-Platform Comparison Simulation")
    print("="*60)
    
    platforms = ["twitter", "tiktok", "instagram"]
    platform_stats = {}
    
    for platform in platforms:
        print(f"\nSimulating {platform}...")
        
        # Adjust config based on platform
        if platform == "twitter":
            config = feed.SimulationConfig(
                num_users=30,
                num_feeds=50,
                duration_hours=24,
                platform=platform,
                with_media_rate=0.30,  # Less media on Twitter
            )
        elif platform == "tiktok":
            config = feed.SimulationConfig(
                num_users=30,
                num_feeds=50,
                duration_hours=24,
                platform=platform,
                with_media_rate=0.95,  # Almost all videos
            )
        else:  # instagram
            config = feed.SimulationConfig(
                num_users=30,
                num_feeds=50,
                duration_hours=24,
                platform=platform,
                with_media_rate=0.80,  # Heavily visual
            )
        
        simulator = feed.SocialSimulator(config)
        feeds, stats = simulator.simulate_activity()
        platform_stats[platform] = stats
    
    # Compare results
    print("\n" + "-"*40)
    print("Platform Comparison:")
    print("-"*40)
    
    for platform, stats in platform_stats.items():
        avg_engagement = stats['total_engagement'] / stats['total_feeds']
        print(f"\n{platform.capitalize()}:")
        print(f"  Average Engagement: {avg_engagement:.1f}")
        print(f"  Media Posts: {stats['total_media']}/{stats['total_feeds']}")
        print(f"  Viral Rate: {stats['viral_feeds']}/{stats['total_feeds']}")


def main():
    """Main function to run all demonstrations"""
    print("\n" + "#"*60)
    print("Feed Module - Social Media Simulation Demo")
    print("#"*60)
    
    # Run different simulation examples
    demonstrate_module_usage()
    run_basic_simulation()
    run_influencer_simulation()
    run_platform_comparison()
    
    print("\n" + "#"*60)
    print("Simulation Complete!")
    print("#"*60)
    print("\nYou can now import and use the feed module in your projects:")
    print("  import feed")
    print("  simulator = feed.SocialSimulator()")
    print("  feeds = simulator.generate_sample_feeds(100)")


if __name__ == "__main__":
    main()
