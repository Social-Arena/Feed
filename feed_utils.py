"""
Feed Utility Functions
Utilities for creating, managing, and persisting feed data
"""

import json
import os
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
import re
import random
import string

from .feed_models import (
    Feed, FeedType, FeedResponse, User, MediaItem, Poll, PollOption,
    Place, Entities, HashtagEntity, MentionEntity, UrlEntity,
    ReferencedFeed, ReferencedFeedType, PublicMetrics, Attachments,
    ContextAnnotation, EditControls, GeoInfo
)


class FeedManager:
    """Manager class for handling feed operations"""
    
    def __init__(self, storage_dir: str = "./feeds"):
        """
        Initialize FeedManager with storage directory
        
        Args:
            storage_dir: Directory to store feed JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def generate_feed_id(self, prefix: str = "") -> str:
        """
        Generate a unique feed ID
        
        Args:
            prefix: Optional prefix for the ID
            
        Returns:
            Unique feed ID
        """
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        unique_part = ''.join(random.choices(string.digits, k=6))
        
        if prefix:
            return f"{prefix}_{timestamp}{unique_part}"
        return f"{timestamp}{unique_part}"
    
    def generate_filename(self, feed_id: Optional[str] = None) -> str:
        """
        Generate filename following the pattern: feed-{time}-{unique_identifier}.json
        
        Args:
            feed_id: Optional feed ID to use in filename
            
        Returns:
            Filename for the feed
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        if feed_id:
            # Extract numeric part from feed_id if available
            numeric_match = re.search(r'\d+', feed_id)
            unique_id = numeric_match.group() if numeric_match else str(uuid.uuid4())[:8]
        else:
            unique_id = str(uuid.uuid4())[:8]
        
        return f"feed-{timestamp}-{unique_id}.json"
    
    def create_feed(
        self,
        text: str,
        author_id: str,
        feed_type: FeedType = FeedType.POST,
        platform: str = "generic",
        **kwargs
    ) -> Feed:
        """
        Create a new feed
        
        Args:
            text: Feed content text
            author_id: ID of the feed author
            feed_type: Type of feed (POST, VIDEO, etc.)
            platform: Platform identifier
            **kwargs: Additional feed properties
            
        Returns:
            Created Feed object
        """
        feed_id = kwargs.pop('id', None) or self.generate_feed_id()
        
        feed = Feed(
            id=feed_id,
            text=text,
            author_id=author_id,
            feed_type=feed_type,
            platform=platform,
            **kwargs
        )
        
        return feed
    
    def save_feed(self, feed: Feed, filename: Optional[str] = None) -> str:
        """
        Save feed to JSON file
        
        Args:
            feed: Feed object to save
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            filename = self.generate_filename(feed.id)
        
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feed.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_feed_response(
        self, 
        response: FeedResponse, 
        filename: Optional[str] = None
    ) -> str:
        """
        Save feed response to JSON file
        
        Args:
            response: FeedResponse object to save
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"feed-response-{timestamp}.json"
        
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_feed(self, filepath: str) -> Feed:
        """
        Load feed from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Feed object
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if it's a response format or single feed
        if 'data' in data and isinstance(data['data'], list):
            # It's a response format, return first feed
            return Feed.from_dict(data['data'][0])
        else:
            # It's a single feed
            return Feed.from_dict(data)
    
    def load_all_feeds(self) -> List[Feed]:
        """
        Load all feeds from storage directory
        
        Returns:
            List of Feed objects
        """
        feeds = []
        
        for filepath in self.storage_dir.glob("feed-*.json"):
            try:
                feed = self.load_feed(str(filepath))
                feeds.append(feed)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        return feeds
    
    def search_feeds(
        self,
        text_contains: Optional[str] = None,
        author_id: Optional[str] = None,
        feed_type: Optional[FeedType] = None,
        platform: Optional[str] = None
    ) -> List[Feed]:
        """
        Search feeds based on criteria
        
        Args:
            text_contains: Text to search for in feed content
            author_id: Filter by author ID
            feed_type: Filter by feed type
            platform: Filter by platform
            
        Returns:
            List of matching Feed objects
        """
        feeds = self.load_all_feeds()
        results = []
        
        for feed in feeds:
            # Apply filters
            if text_contains and text_contains.lower() not in feed.text.lower():
                continue
            if author_id and feed.author_id != author_id:
                continue
            if feed_type and feed.feed_type != feed_type:
                continue
            if platform and feed.platform != platform:
                continue
            
            results.append(feed)
        
        return results


def extract_entities(text: str) -> Entities:
    """
    Extract entities (hashtags, mentions, URLs) from text
    
    Args:
        text: Text to extract entities from
        
    Returns:
        Entities object containing extracted entities
    """
    entities = Entities()
    
    # Extract hashtags
    hashtag_pattern = r'#(\w+)'
    for match in re.finditer(hashtag_pattern, text):
        entities.hashtags.append(HashtagEntity(
            start=match.start(),
            end=match.end(),
            tag=match.group(1)
        ))
    
    # Extract mentions
    mention_pattern = r'@(\w+)'
    for match in re.finditer(mention_pattern, text):
        entities.mentions.append(MentionEntity(
            start=match.start(),
            end=match.end(),
            username=match.group(1),
            id=str(abs(hash(match.group(1))))  # Generate consistent ID from username
        ))
    
    # Extract URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    for match in re.finditer(url_pattern, text):
        url = match.group()
        entities.urls.append(UrlEntity(
            start=match.start(),
            end=match.end(),
            url=url[:30] + "..." if len(url) > 30 else url,  # Shortened URL
            expanded_url=url,
            display_url=url.replace("https://", "").replace("http://", "")[:30]
        ))
    
    return entities if (entities.hashtags or entities.mentions or entities.urls) else None


def create_sample_user(
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    name: Optional[str] = None
) -> User:
    """
    Create a sample user
    
    Args:
        user_id: Optional user ID
        username: Optional username
        name: Optional display name
        
    Returns:
        User object
    """
    if not user_id:
        user_id = str(random.randint(100000, 999999))
    if not username:
        username = f"user_{user_id[-6:]}"
    if not name:
        name = f"User {user_id[-4:]}"
    
    return User(
        id=user_id,
        username=username,
        name=name,
        verified=random.choice([True, False]),
        description=f"Sample user profile for {username}",
        created_at=datetime.utcnow().isoformat() + "Z",
        public_metrics={
            "followers_count": random.randint(100, 10000),
            "following_count": random.randint(50, 1000),
            "tweet_count": random.randint(10, 5000),
            "listed_count": random.randint(0, 100)
        }
    )


def create_sample_media(media_type: str = "photo") -> MediaItem:
    """
    Create a sample media item
    
    Args:
        media_type: Type of media (photo, video, etc.)
        
    Returns:
        MediaItem object
    """
    media_key = f"3_{random.randint(10**18, 10**19-1)}"
    
    media = MediaItem(
        media_key=media_key,
        type=media_type,
        url=f"https://example.com/media/{media_key}",
        height=1080 if media_type == "photo" else 1920,
        width=1920 if media_type == "photo" else 1080
    )
    
    if media_type == "video":
        media.duration_ms = random.randint(5000, 60000)
        media.preview_image_url = f"https://example.com/media/{media_key}/preview.jpg"
        media.variants = [
            {"bit_rate": 2176000, "content_type": "video/mp4", "url": f"https://example.com/media/{media_key}/720p.mp4"},
            {"bit_rate": 832000, "content_type": "video/mp4", "url": f"https://example.com/media/{media_key}/480p.mp4"},
            {"bit_rate": 288000, "content_type": "video/mp4", "url": f"https://example.com/media/{media_key}/240p.mp4"}
        ]
    
    return media


def create_thread(
    texts: List[str],
    author_id: str,
    manager: FeedManager,
    platform: str = "twitter"
) -> List[Feed]:
    """
    Create a thread of connected feeds
    
    Args:
        texts: List of text content for each feed in the thread
        author_id: Author ID for all feeds in the thread
        manager: FeedManager instance
        platform: Platform identifier
        
    Returns:
        List of Feed objects forming the thread
    """
    thread = []
    conversation_id = None
    
    for i, text in enumerate(texts):
        feed = manager.create_feed(
            text=text,
            author_id=author_id,
            feed_type=FeedType.THREAD if i > 0 else FeedType.POST,
            platform=platform
        )
        
        if i == 0:
            # First post starts the conversation
            conversation_id = feed.id
            feed.conversation_id = conversation_id
        else:
            # Subsequent posts reply to the previous one
            feed.conversation_id = conversation_id
            feed.in_reply_to_user_id = author_id
            feed.referenced_feeds = [
                ReferencedFeed(
                    type=ReferencedFeedType.REPLIED_TO.value,
                    id=thread[-1].id
                )
            ]
        
        # Extract entities from text
        feed.entities = extract_entities(text)
        
        thread.append(feed)
    
    return thread
