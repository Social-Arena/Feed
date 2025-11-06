"""
FeedManager - Core manager for creating, saving, and loading feeds
"""

import json
import re
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from ..models import Feed, FeedType
from .generators import generate_feed_id


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
            unique_id = numeric_match.group() if numeric_match else feed_id[:13]
        else:
            unique_id = generate_feed_id()[:13]
        
        return f"feed-{timestamp}-{unique_id}.json"
    
    def create_feed(
        self,
        text: str,
        author_id: str,
        feed_type: FeedType = FeedType.POST,
        **kwargs
    ) -> Feed:
        """
        Create a new feed
        
        Args:
            text: Feed content text
            author_id: ID of the feed author
            feed_type: Type of feed (POST, REPLY, etc.)
            **kwargs: Additional feed properties
            
        Returns:
            Created Feed object
        """
        feed_id = kwargs.pop('id', None) or generate_feed_id()
        
        feed = Feed(
            id=feed_id,
            text=text,
            author_id=author_id,
            feed_type=feed_type,
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
        feed_type: Optional[FeedType] = None
    ) -> List[Feed]:
        """
        Search feeds based on criteria
        
        Args:
            text_contains: Text to search for in feed content
            author_id: Filter by author ID
            feed_type: Filter by feed type
            
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
            
            results.append(feed)
        
        return results

