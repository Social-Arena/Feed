"""
Tests for Feed data structure
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import feed


def test_create_feed():
    """Test basic feed creation"""
    manager = feed.FeedManager()
    tweet = manager.create_feed(
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
    manager = feed.FeedManager()
    original = manager.create_feed(
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


def test_feed_manager():
    """Test FeedManager operations"""
    manager = feed.FeedManager(storage_dir="./test_feeds")
    
    # Create
    tweet = manager.create_feed(
        text="Test tweet for manager",
        author_id="user_456"
    )
    
    # Save
    filepath = manager.save_feed(tweet)
    assert os.path.exists(filepath)
    
    # Load
    loaded = manager.load_feed(filepath)
    assert loaded.id == tweet.id
    assert loaded.text == tweet.text
    
    # Cleanup
    os.remove(filepath)
    print("✓ test_feed_manager passed")


def test_reply_structure():
    """Test reply tweet structure"""
    manager = feed.FeedManager()
    
    # Original tweet
    original = manager.create_feed(
        text="Original tweet",
        author_id="user_1"
    )
    
    # Reply
    reply = manager.create_feed(
        text="@user_1 This is a reply",
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
    
    assert reply.conversation_id == original.id
    assert reply.in_reply_to_user_id == "user_1"
    assert len(reply.referenced_feeds) == 1
    assert reply.referenced_feeds[0].type == feed.ReferencedFeedType.REPLIED_TO.value
    print("✓ test_reply_structure passed")


def test_user_model():
    """Test User model"""
    user = feed.create_sample_user(
        user_id="12345",
        username="testuser",
        name="Test User"
    )
    
    assert user.id == "12345"
    assert user.username == "testuser"
    assert user.name == "Test User"
    assert user.public_metrics is not None
    print("✓ test_user_model passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Feed Package Tests (Data Structure Only)")
    print("="*60 + "\n")
    
    test_create_feed()
    test_entity_extraction()
    test_feed_serialization()
    test_feed_manager()
    test_reply_structure()
    test_user_model()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
