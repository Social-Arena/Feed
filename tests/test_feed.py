"""
Basic tests for Feed model
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import feed


def test_create_feed():
    """Test basic feed creation"""
    tweet = feed.create_tweet(
        text="Test tweet #testing",
        author_id="test_user"
    )
    
    assert tweet.id is not None
    assert tweet.text == "Test tweet #testing"
    assert tweet.author_id == "test_user"
    assert tweet.feed_type == feed.FeedType.POST
    print("✓ test_create_feed passed")


def test_entity_extraction():
    """Test entity extraction"""
    text = "Hello @user check #python and https://example.com"
    entities = feed.extract_entities(text)
    
    assert entities is not None
    assert len(entities.hashtags) == 1
    assert len(entities.mentions) == 1
    assert len(entities.urls) == 1
    assert entities.hashtags[0].tag == "python"
    assert entities.mentions[0].username == "user"
    print("✓ test_entity_extraction passed")


def test_feed_serialization():
    """Test feed to_dict and from_dict"""
    original = feed.create_tweet(
        text="Serialization test",
        author_id="user_123"
    )
    
    # Convert to dict and back
    data = original.to_dict()
    loaded = feed.Feed.from_dict(data)
    
    assert loaded.id == original.id
    assert loaded.text == original.text
    assert loaded.author_id == original.author_id
    print("✓ test_feed_serialization passed")


def test_simulation():
    """Test basic simulation"""
    tweets, stats = feed.simulate_twitter(num_tweets=10, num_users=5)
    
    assert len(tweets) == 10
    assert stats['total_tweets'] == 10
    assert stats['total_engagement'] >= 0
    print("✓ test_simulation passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Feed Package Tests")
    print("="*60 + "\n")
    
    test_create_feed()
    test_entity_extraction()
    test_feed_serialization()
    test_simulation()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()

