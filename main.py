#!/usr/bin/env python3
"""
Feed Data Structure Implementation
Main script for creating and managing feed data
"""

import json
from datetime import datetime, timedelta
import random
from typing import List

from feed_models import (
    Feed, FeedType, FeedResponse, User, MediaItem,
    Poll, PollOption, Place, GeoInfo, PublicMetrics,
    Attachments, ReferencedFeed, ReferencedFeedType,
    ContextAnnotation, EditControls
)
from feed_utils import (
    FeedManager, extract_entities, create_sample_user,
    create_sample_media, create_thread
)


def create_example_feeds():
    """Create various example feeds demonstrating different features"""
    
    manager = FeedManager()
    feeds = []
    users = []
    media_items = []
    places = []
    
    # Create sample users
    user1 = create_sample_user("123456", "techuser", "Tech Enthusiast")
    user2 = create_sample_user("789012", "newsbot", "News Bot")
    user3 = create_sample_user("345678", "influencer", "Social Influencer")
    users.extend([user1, user2, user3])
    
    # Example 1: Simple text post
    feed1 = manager.create_feed(
        text="Hello, world! This is my first feed post. #FirstPost #HelloWorld",
        author_id=user1.id,
        feed_type=FeedType.POST,
        platform="twitter"
    )
    feed1.entities = extract_entities(feed1.text)
    feed1.public_metrics = PublicMetrics(
        repost_count=5,
        reply_count=2,
        like_count=15,
        quote_count=1
    )
    feed1.lang = "en"
    feed1.source = "Feed Web App"
    feeds.append(feed1)
    
    # Example 2: Post with media (photo)
    media1 = create_sample_media("photo")
    media_items.append(media1)
    
    feed2 = manager.create_feed(
        text="Check out this amazing sunset! 🌅 #Photography #Nature #Sunset @photoclub",
        author_id=user3.id,
        feed_type=FeedType.IMAGE_POST,
        platform="instagram"
    )
    feed2.entities = extract_entities(feed2.text)
    feed2.attachments = Attachments(media_keys=[media1.media_key])
    feed2.public_metrics = PublicMetrics(
        repost_count=25,
        reply_count=8,
        like_count=250,
        quote_count=3,
        bookmark_count=15
    )
    feed2.possibly_sensitive = False
    feeds.append(feed2)
    
    # Example 3: Video post (TikTok-style)
    media2 = create_sample_media("video")
    media_items.append(media2)
    
    feed3 = manager.create_feed(
        text="New dance challenge! 💃 Who's joining? #DanceChallenge #Viral #ForYou",
        author_id=user3.id,
        feed_type=FeedType.VIDEO,
        platform="tiktok"
    )
    feed3.entities = extract_entities(feed3.text)
    feed3.attachments = Attachments(media_keys=[media2.media_key])
    feed3.public_metrics = PublicMetrics(
        repost_count=500,
        reply_count=125,
        like_count=5000,
        view_count=50000,
        share_count=200
    )
    feed3.platform_specific_data = {
        "music_id": "7890123456",
        "effect_ids": ["effect_123", "effect_456"],
        "duet_enabled": True,
        "stitch_enabled": True
    }
    feeds.append(feed3)
    
    # Example 4: Reply to another post
    feed4 = manager.create_feed(
        text="Great photo! Where was this taken? 📍",
        author_id=user1.id,
        feed_type=FeedType.POST,
        platform="twitter"
    )
    feed4.conversation_id = feed2.id
    feed4.in_reply_to_user_id = user3.id
    feed4.referenced_feeds = [
        ReferencedFeed(type=ReferencedFeedType.REPLIED_TO.value, id=feed2.id)
    ]
    feed4.entities = extract_entities(feed4.text)
    feeds.append(feed4)
    
    # Example 5: Quote/Repost with comment
    feed5 = manager.create_feed(
        text="This is exactly what I was talking about! Machine learning is revolutionizing everything 🤖 https://example.com/ml-article",
        author_id=user2.id,
        feed_type=FeedType.POST,
        platform="twitter"
    )
    feed5.referenced_feeds = [
        ReferencedFeed(type=ReferencedFeedType.QUOTED.value, id=feed1.id)
    ]
    feed5.entities = extract_entities(feed5.text)
    feed5.context_annotations = [
        ContextAnnotation(
            domain={"id": "46", "name": "Technology", "description": "Technology and computing"},
            entity={"id": "1", "name": "Machine Learning", "description": "ML and AI topics"}
        )
    ]
    feeds.append(feed5)
    
    # Example 6: Post with location
    place1 = Place(
        id="01a9a39529b27f36",
        full_name="New York, NY",
        name="New York",
        country="United States",
        country_code="US",
        place_type="city"
    )
    places.append(place1)
    
    feed6 = manager.create_feed(
        text="Live from Times Square! 🗽 The energy here is incredible! #NYC #TimesSquare",
        author_id=user3.id,
        feed_type=FeedType.POST,
        platform="twitter"
    )
    feed6.entities = extract_entities(feed6.text)
    feed6.geo = GeoInfo(
        place_id=place1.id,
        coordinates={"type": "Point", "coordinates": [-73.985130, 40.758896]}
    )
    feed6.public_metrics = PublicMetrics(
        repost_count=15,
        reply_count=7,
        like_count=89,
        impressions=1250
    )
    feeds.append(feed6)
    
    # Example 7: Post with poll
    poll1 = Poll(
        id="poll_" + manager.generate_feed_id(),
        options=[
            PollOption(position=1, label="Python", votes=245),
            PollOption(position=2, label="JavaScript", votes=189),
            PollOption(position=3, label="Rust", votes=97),
            PollOption(position=4, label="Go", votes=63)
        ],
        duration_minutes=1440,  # 24 hours
        end_datetime=(datetime.utcnow() + timedelta(days=1)).isoformat() + "Z",
        voting_status="open"
    )
    
    feed7 = manager.create_feed(
        text="What's your favorite programming language for backend development? Vote below! 👇 #Programming #Tech #Poll",
        author_id=user1.id,
        feed_type=FeedType.POST,
        platform="twitter"
    )
    feed7.entities = extract_entities(feed7.text)
    feed7.attachments = Attachments(poll_ids=[poll1.id])
    feed7.public_metrics = PublicMetrics(
        repost_count=45,
        reply_count=32,
        like_count=156
    )
    feeds.append(feed7)
    
    # Example 8: Edited post
    feed8 = manager.create_feed(
        text="BREAKING: Major announcement coming soon! Stay tuned... (Edit: Added more details in thread below)",
        author_id=user2.id,
        feed_type=FeedType.POST,
        platform="twitter"
    )
    feed8.entities = extract_entities(feed8.text)
    feed8.edit_history_feed_ids = [feed8.id, feed8.id + "_v1"]
    feed8.edit_controls = EditControls(
        edits_remaining=3,
        is_edit_eligible=True,
        editable_until=(datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    )
    feed8.possibly_sensitive = False
    feed8.reply_settings = "everyone"
    feeds.append(feed8)
    
    # Create a thread
    thread_texts = [
        "🧵 Thread: Understanding the Feed Data Structure (1/3)",
        "The Feed structure is designed to be platform-agnostic while supporting features from Twitter, Instagram, TikTok, and more. (2/3)",
        "This allows for unified data handling across different social media platforms. Check out the documentation for more details! (3/3)"
    ]
    thread_feeds = create_thread(thread_texts, user1.id, manager, "twitter")
    feeds.extend(thread_feeds)
    
    # Save individual feed files
    print("Saving individual feed files...")
    for feed in feeds:
        filepath = manager.save_feed(feed)
        print(f"  Saved: {filepath}")
    
    # Create and save a feed response (API-style)
    response = FeedResponse(
        data=feeds[:5],  # Include first 5 feeds
        includes={
            "users": [user.to_dict() for user in users],
            "media": [media.to_dict() for media in media_items],
            "places": [place.to_dict() for place in places],
            "polls": [poll1.to_dict()]
        },
        meta={
            "result_count": len(feeds[:5]),
            "newest_id": feeds[0].id,
            "oldest_id": feeds[4].id if len(feeds) >= 5 else feeds[-1].id,
            "next_token": "next_page_token_example"
        }
    )
    
    response_file = manager.save_feed_response(response)
    print(f"\nSaved feed response: {response_file}")
    
    return feeds, response


def demonstrate_feed_operations():
    """Demonstrate various feed operations"""
    
    manager = FeedManager()
    
    print("\n" + "="*60)
    print("Feed Data Structure Demo")
    print("="*60)
    
    # Create example feeds
    feeds, response = create_example_feeds()
    
    print(f"\nCreated {len(feeds)} example feeds")
    
    # Demonstrate loading feeds
    print("\n" + "-"*40)
    print("Loading feeds from storage...")
    loaded_feeds = manager.load_all_feeds()
    print(f"Loaded {len(loaded_feeds)} feeds from storage")
    
    # Demonstrate searching
    print("\n" + "-"*40)
    print("Searching feeds...")
    
    # Search by text
    results = manager.search_feeds(text_contains="challenge")
    print(f"Found {len(results)} feeds containing 'challenge'")
    for feed in results:
        print(f"  - {feed.id}: {feed.text[:50]}...")
    
    # Search by platform
    results = manager.search_feeds(platform="twitter")
    print(f"\nFound {len(results)} feeds from Twitter")
    
    # Search by feed type
    results = manager.search_feeds(feed_type=FeedType.VIDEO)
    print(f"Found {len(results)} video feeds")
    
    # Display sample JSON structure
    print("\n" + "-"*40)
    print("Sample Feed JSON Structure:")
    print("-"*40)
    
    sample_feed = feeds[0]
    print(json.dumps(sample_feed.to_dict(), indent=2))
    
    print("\n" + "-"*40)
    print("Sample Feed Response JSON Structure (with includes):")
    print("-"*40)
    
    response_sample = {
        "data": [feeds[0].to_dict()],
        "includes": {
            "users": [{"id": "123456", "username": "techuser", "name": "Tech Enthusiast"}],
            "media": [],
            "places": []
        },
        "meta": {
            "result_count": 1,
            "newest_id": feeds[0].id,
            "oldest_id": feeds[0].id
        }
    }
    print(json.dumps(response_sample, indent=2))
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60)


if __name__ == "__main__":
    demonstrate_feed_operations()
