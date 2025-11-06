#!/usr/bin/env python3
"""
Twitter simulation demonstration
"""

import feed


def simple_simulation():
    """Run a simple Twitter simulation"""
    print("=" * 60)
    print("Simple Twitter Simulation")
    print("=" * 60)
    
    # Quick simulation
    tweets, stats = feed.simulate_twitter(num_tweets=50, num_users=20)
    
    print(f"\nSimulation completed!")
    print(f"Total tweets: {stats['total_tweets']}")
    print(f"Total replies: {stats['total_replies']}")
    print(f"Total quotes: {stats['total_quotes']}")
    print(f"Total engagement: {stats['total_engagement']:,}")
    print(f"Viral tweets: {stats['viral_tweets']}")
    
    # Show a sample tweet
    if tweets:
        sample = tweets[len(tweets) // 2]
        print(f"\nSample tweet:")
        print(f"  Author: user_{sample.author_id}")
        print(f"  Text: {sample.text}")
        print(f"  Likes: {sample.public_metrics.like_count}")
        print(f"  Retweets: {sample.public_metrics.retweet_count}")
    print()


def advanced_simulation():
    """Run an advanced simulation with custom configuration"""
    print("=" * 60)
    print("Advanced Twitter Simulation")
    print("=" * 60)
    
    # Custom configuration
    config = feed.SimulationConfig(
        num_users=100,
        num_tweets=500,
        duration_hours=24,
        like_rate=0.20,  # 20% like rate
        retweet_rate=0.05,  # 5% retweet rate
        reply_probability=0.25,  # 25% of tweets are replies
    )
    
    simulator = feed.TwitterSimulator(config)
    
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
    print(f"\nSimulating {config.num_tweets} tweets over {config.duration_hours} hours...")
    tweets, stats = simulator.simulate()
    
    # Display statistics
    print("\n" + "-" * 40)
    print("Simulation Statistics:")
    print("-" * 40)
    print(f"Total Tweets: {stats['total_tweets']}")
    print(f"Total Replies: {stats['total_replies']}")
    print(f"Total Quotes: {stats['total_quotes']}")
    print(f"Total Engagement: {stats['total_engagement']:,}")
    print(f"Viral Tweets: {stats['viral_tweets']}")
    
    print(f"\nTop 5 Active Hours:")
    sorted_hours = sorted(stats['by_hour'].items(), key=lambda x: x[1], reverse=True)[:5]
    for hour, count in sorted_hours:
        print(f"  {hour:02d}:00 - {count} tweets")
    
    # Find most engaged tweets
    top_tweets = sorted(tweets, key=lambda t: t.public_metrics.like_count, reverse=True)[:5]
    
    print("\nTop 5 Most Liked Tweets:")
    for i, tweet in enumerate(top_tweets, 1):
        print(f"\n{i}. {tweet.text[:80]}...")
        print(f"   Likes: {tweet.public_metrics.like_count:,}")
        print(f"   Retweets: {tweet.public_metrics.retweet_count:,}")
    
    # Save results
    print("\n" + "-" * 40)
    print("Saving simulation results...")
    result = simulator.save_results(save_individual=True)
    print(f"Saved {len(result['saved_files'])} tweet files")
    print()


def influencer_simulation():
    """Simulate influencer behavior"""
    print("=" * 60)
    print("Influencer-Focused Simulation")
    print("=" * 60)
    
    config = feed.SimulationConfig(
        num_users=30,
        num_tweets=200,
        duration_hours=48,
        like_rate=0.30,  # Higher engagement
    )
    
    simulator = feed.TwitterSimulator(config)
    
    # Create some influencers manually
    influencers = []
    for i in range(5):
        influencer = feed.UserBehavior(
            user_id=f"influencer_{i}",
            username=f"influencer_{i}",
            activity_level="influencer",
            interests=["technology", "entertainment"],
            posting_frequency=5.0,
            engagement_probability=0.8,
            follower_count=100000 + i * 50000,
            following_count=500,
        )
        influencers.append(influencer)
    
    # Add to simulator
    simulator.users.extend(influencers)
    simulator.generate_users(25)  # Add regular users
    
    print(f"Created {len(influencers)} influencers and 25 regular users")
    
    # Run simulation
    tweets, stats = simulator.simulate()
    
    # Find influencer tweets
    influencer_tweets = [t for t in tweets if t.author_id.startswith("influencer_")]
    avg_engagement = sum(t.public_metrics.like_count for t in influencer_tweets) / len(influencer_tweets) if influencer_tweets else 0
    
    print(f"\nInfluencer Statistics:")
    print(f"  Total influencer tweets: {len(influencer_tweets)}")
    print(f"  Average likes per tweet: {avg_engagement:.1f}")
    print()


def main():
    """Run all simulation demos"""
    print("\n" + "=" * 60)
    print("Feed Package - Twitter Simulation Demo")
    print("=" * 60 + "\n")
    
    simple_simulation()
    advanced_simulation()
    influencer_simulation()
    
    print("=" * 60)
    print("Simulation demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

