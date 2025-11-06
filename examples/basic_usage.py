#!/usr/bin/env python3
"""
Basic usage examples for the Feed package
"""

import feed


def example_create_tweet():
    """Example 1: Create a simple tweet"""
    print("=" * 60)
    print("Example 1: Creating a Simple Tweet")
    print("=" * 60)
    
    tweet = feed.create_tweet(
        text="Hello Twitter! This is my first tweet using the Feed package. #Python #TwitterAPI",
        author_id="user_12345"
    )
    
    print(f"Created tweet with ID: {tweet.id}")
    print(f"Text: {tweet.text}")
    print(f"Author: {tweet.author_id}")
    print(f"Created at: {tweet.created_at}")
    print()


def example_entity_extraction():
    """Example 2: Extract entities from text"""
    print("=" * 60)
    print("Example 2: Entity Extraction")
    print("=" * 60)
    
    text = "Check out @elonmusk's thoughts on #AI and #MachineLearning! https://example.com/article"
    entities = feed.extract_entities(text)
    
    if entities:
        print(f"Text: {text}\n")
        print(f"Hashtags: {[h.tag for h in entities.hashtags]}")
        print(f"Mentions: {[m.username for m in entities.mentions]}")
        print(f"URLs: {[u.expanded_url for u in entities.urls]}")
    print()


def example_reply_tweet():
    """Example 3: Create a reply tweet"""
    print("=" * 60)
    print("Example 3: Creating a Reply Tweet")
    print("=" * 60)
    
    manager = feed.FeedManager()
    
    # Original tweet
    original = manager.create_feed(
        text="What's everyone working on today? #MondayMotivation",
        author_id="user_1"
    )
    
    # Reply tweet
    reply = manager.create_feed(
        text="@user_1 Working on a Twitter simulation project! It's going great 🚀",
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
    
    print(f"Original tweet: {original.text}")
    print(f"Reply tweet: {reply.text}")
    print(f"Conversation ID: {reply.conversation_id}")
    print()


def example_save_and_load():
    """Example 4: Save and load tweets"""
    print("=" * 60)
    print("Example 4: Save and Load Tweets")
    print("=" * 60)
    
    manager = feed.FeedManager(storage_dir="./example_tweets")
    
    # Create and save a tweet
    tweet = manager.create_feed(
        text="Testing save and load functionality! #Python",
        author_id="user_123"
    )
    
    filepath = manager.save_feed(tweet)
    print(f"Saved tweet to: {filepath}")
    
    # Load the tweet back
    loaded_tweet = manager.load_feed(filepath)
    print(f"Loaded tweet text: {loaded_tweet.text}")
    print()


def example_with_metrics():
    """Example 5: Tweet with engagement metrics"""
    print("=" * 60)
    print("Example 5: Tweet with Engagement Metrics")
    print("=" * 60)
    
    tweet = feed.create_tweet(
        text="Just shipped a new feature! 🎉 #ProductLaunch",
        author_id="user_456"
    )
    
    # Set engagement metrics
    tweet.public_metrics = feed.PublicMetrics(
        like_count=150,
        retweet_count=45,
        reply_count=23,
        quote_count=8,
        bookmark_count=12,
        impression_count=5000
    )
    
    print(f"Tweet: {tweet.text}")
    print(f"Likes: {tweet.public_metrics.like_count}")
    print(f"Retweets: {tweet.public_metrics.retweet_count}")
    print(f"Replies: {tweet.public_metrics.reply_count}")
    print(f"Impressions: {tweet.public_metrics.impression_count}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Feed Package - Basic Usage Examples")
    print("=" * 60 + "\n")
    
    example_create_tweet()
    example_entity_extraction()
    example_reply_tweet()
    example_save_and_load()
    example_with_metrics()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

