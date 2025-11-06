"""
Core Feed data structure - Twitter-focused
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

from .entities import Entities
from .metrics import PublicMetrics
from .references import ReferencedFeed


class FeedType(Enum):
    """Types of feeds supported for Twitter simulation"""
    POST = "post"           # Standard tweet
    REPLY = "reply"         # Reply to another tweet
    QUOTE = "quote"         # Quote tweet
    RETWEET = "retweet"     # Retweet
    THREAD = "thread"       # Thread continuation


@dataclass
class Feed:
    """
    Main Feed data structure - Twitter tweet equivalent
    Simplified and focused on Twitter simulation
    """
    # Core fields (always present)
    id: str
    text: str
    author_id: str
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    feed_type: FeedType = FeedType.POST
    
    # Conversation and threading
    conversation_id: Optional[str] = None
    in_reply_to_user_id: Optional[str] = None
    
    # References to other feeds
    referenced_feeds: List[ReferencedFeed] = field(default_factory=list)
    
    # Content entities
    entities: Optional[Entities] = None
    
    # Metrics
    public_metrics: PublicMetrics = field(default_factory=PublicMetrics)
    
    # Twitter-specific features
    lang: str = "en"
    source: str = "Twitter Web App"
    possibly_sensitive: bool = False
    
    # Platform identifier
    platform: str = "twitter"
    
    def __post_init__(self):
        """Auto-generate conversation_id if not provided"""
        if self.conversation_id is None:
            self.conversation_id = self.id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Feed to dictionary for JSON serialization"""
        from dataclasses import asdict
        
        data = {
            "id": self.id,
            "text": self.text,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "feed_type": self.feed_type.value,
            "conversation_id": self.conversation_id,
            "in_reply_to_user_id": self.in_reply_to_user_id,
            "referenced_feeds": [asdict(rf) for rf in self.referenced_feeds],
            "entities": self.entities.to_dict() if self.entities else None,
            "public_metrics": asdict(self.public_metrics),
            "lang": self.lang,
            "source": self.source,
            "possibly_sensitive": self.possibly_sensitive,
            "platform": self.platform
        }
        
        # Remove None values for cleaner JSON
        return {k: v for k, v in data.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feed':
        """Create Feed from dictionary"""
        from .entities import Entities, HashtagEntity, MentionEntity, UrlEntity
        from .metrics import PublicMetrics
        from .references import ReferencedFeed
        
        # Convert string feed_type to enum
        if 'feed_type' in data and isinstance(data['feed_type'], str):
            data['feed_type'] = FeedType(data['feed_type'])
        
        # Convert entities
        if data.get('entities'):
            entities_data = data['entities']
            data['entities'] = Entities(
                hashtags=[HashtagEntity(**h) for h in entities_data.get('hashtags', [])],
                mentions=[MentionEntity(**m) for m in entities_data.get('mentions', [])],
                urls=[UrlEntity(**u) for u in entities_data.get('urls', [])]
            )
        
        # Convert other complex fields
        if data.get('referenced_feeds'):
            data['referenced_feeds'] = [ReferencedFeed(**rf) for rf in data['referenced_feeds']]
        
        if data.get('public_metrics'):
            data['public_metrics'] = PublicMetrics(**data['public_metrics'])
        
        return cls(**data)

