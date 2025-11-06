"""
Feed Data Models
Equivalent to Twitter/X Tweet data structure with support for various social media platforms
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from enum import Enum
import json
import uuid


class FeedType(Enum):
    """Types of feeds supported"""
    POST = "post"           # Standard text post (Tweet-like)
    VIDEO = "video"         # Video content (TikTok-like)
    IMAGE_POST = "image_post"  # Image-focused post (Instagram-like)
    STORY = "story"         # Ephemeral content
    REEL = "reel"          # Short video (Instagram Reels)
    THREAD = "thread"       # Connected series of posts


class ReferencedFeedType(Enum):
    """Types of references between feeds"""
    REPLIED_TO = "replied_to"
    QUOTED = "quoted"
    REPOSTED = "reposted"  # Equivalent to retweet
    SHARED = "shared"


@dataclass
class HashtagEntity:
    """Hashtag entity in feed content"""
    start: int
    end: int
    tag: str


@dataclass
class MentionEntity:
    """User mention entity in feed content"""
    start: int
    end: int
    username: str
    id: str


@dataclass
class UrlEntity:
    """URL entity in feed content"""
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str
    title: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Entities:
    """Container for all entities in feed content"""
    hashtags: List[HashtagEntity] = field(default_factory=list)
    mentions: List[MentionEntity] = field(default_factory=list)
    urls: List[UrlEntity] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "hashtags": [asdict(h) for h in self.hashtags],
            "mentions": [asdict(m) for m in self.mentions],
            "urls": [asdict(u) for u in self.urls]
        }


@dataclass
class MediaItem:
    """Media item attached to a feed"""
    media_key: str
    type: Literal["photo", "video", "animated_gif", "audio"]
    url: Optional[str] = None
    preview_image_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    duration_ms: Optional[int] = None
    alt_text: Optional[str] = None
    variants: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert MediaItem to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class PollOption:
    """Poll option in a feed poll"""
    position: int
    label: str
    votes: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert PollOption to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class Poll:
    """Poll attached to a feed"""
    id: str
    options: List[PollOption]
    duration_minutes: int
    end_datetime: str
    voting_status: Literal["open", "closed"]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Poll to dictionary for JSON serialization"""
        data = asdict(self)
        data['options'] = [opt.to_dict() for opt in self.options]
        return data


@dataclass
class Place:
    """Geographic place information"""
    id: str
    full_name: str
    name: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    place_type: Optional[str] = None
    contained_within: List[str] = field(default_factory=list)
    geo: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Place to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class GeoInfo:
    """Geographic information for a feed"""
    place_id: Optional[str] = None
    coordinates: Optional[Dict[str, Any]] = None  # {"type": "Point", "coordinates": [lon, lat]}


@dataclass
class PublicMetrics:
    """Public engagement metrics for a feed"""
    repost_count: int = 0      # Retweet equivalent
    reply_count: int = 0
    like_count: int = 0
    quote_count: int = 0
    bookmark_count: int = 0
    impressions: Optional[int] = None
    view_count: Optional[int] = None  # For videos
    share_count: Optional[int] = None


@dataclass
class ReferencedFeed:
    """Reference to another feed (reply, quote, repost)"""
    type: str  # ReferencedFeedType value
    id: str


@dataclass
class ContextAnnotation:
    """Context annotations for feed content understanding"""
    domain: Dict[str, str]  # {"id": "...", "name": "...", "description": "..."}
    entity: Dict[str, str]  # {"id": "...", "name": "...", "description": "..."}


@dataclass
class EditControls:
    """Edit history and controls for a feed"""
    edits_remaining: int
    is_edit_eligible: bool
    editable_until: str  # ISO 8601 datetime


@dataclass
class User:
    """User/Author information"""
    id: str
    username: str
    name: str
    profile_image_url: Optional[str] = None
    verified: bool = False
    verified_type: Optional[Literal["blue", "business", "government"]] = None
    description: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    public_metrics: Optional[Dict[str, int]] = None  # followers_count, following_count, etc.
    location: Optional[str] = None
    pinned_feed_ids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert User to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class Attachments:
    """Container for feed attachments"""
    media_keys: List[str] = field(default_factory=list)
    poll_ids: List[str] = field(default_factory=list)


@dataclass
class Feed:
    """
    Main Feed data structure - equivalent to a Tweet/Post
    """
    # Core fields (always present)
    id: str
    text: str
    
    # Metadata
    feed_type: FeedType = FeedType.POST
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    author_id: str = ""
    
    # Conversation and threading
    conversation_id: Optional[str] = None
    in_reply_to_user_id: Optional[str] = None
    
    # References to other feeds
    referenced_feeds: List[ReferencedFeed] = field(default_factory=list)
    
    # Content entities
    entities: Optional[Entities] = None
    
    # Attachments
    attachments: Optional[Attachments] = None
    
    # Geographic information
    geo: Optional[GeoInfo] = None
    
    # Metrics
    public_metrics: PublicMetrics = field(default_factory=PublicMetrics)
    
    # Platform-specific features
    lang: Optional[str] = None
    source: Optional[str] = None  # Client used to post
    possibly_sensitive: bool = False
    reply_settings: Optional[Literal["everyone", "mentioned_users", "followers"]] = None
    
    # Context and categorization
    context_annotations: List[ContextAnnotation] = field(default_factory=list)
    
    # Edit history
    edit_history_feed_ids: List[str] = field(default_factory=list)
    edit_controls: Optional[EditControls] = None
    
    # Content moderation
    withheld: Optional[Dict[str, Any]] = None
    
    # Platform-specific fields
    platform: str = "generic"  # twitter, tiktok, instagram, etc.
    platform_specific_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        # Auto-generate conversation_id if not provided
        if self.conversation_id is None:
            self.conversation_id = self.id
        
        # Initialize edit history with current ID if empty
        if not self.edit_history_feed_ids:
            self.edit_history_feed_ids = [self.id]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Feed to dictionary for JSON serialization"""
        data = {
            "id": self.id,
            "text": self.text,
            "feed_type": self.feed_type.value,
            "created_at": self.created_at,
            "author_id": self.author_id,
            "conversation_id": self.conversation_id,
            "in_reply_to_user_id": self.in_reply_to_user_id,
            "referenced_feeds": [asdict(rf) for rf in self.referenced_feeds],
            "entities": self.entities.to_dict() if self.entities else None,
            "attachments": asdict(self.attachments) if self.attachments else None,
            "geo": asdict(self.geo) if self.geo else None,
            "public_metrics": asdict(self.public_metrics),
            "lang": self.lang,
            "source": self.source,
            "possibly_sensitive": self.possibly_sensitive,
            "reply_settings": self.reply_settings,
            "context_annotations": [asdict(ca) for ca in self.context_annotations],
            "edit_history_feed_ids": self.edit_history_feed_ids,
            "edit_controls": asdict(self.edit_controls) if self.edit_controls else None,
            "withheld": self.withheld,
            "platform": self.platform,
            "platform_specific_data": self.platform_specific_data
        }
        
        # Remove None values for cleaner JSON
        return {k: v for k, v in data.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feed':
        """Create Feed from dictionary"""
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
        
        if data.get('attachments'):
            data['attachments'] = Attachments(**data['attachments'])
        
        if data.get('geo'):
            data['geo'] = GeoInfo(**data['geo'])
        
        if data.get('public_metrics'):
            data['public_metrics'] = PublicMetrics(**data['public_metrics'])
        
        if data.get('context_annotations'):
            data['context_annotations'] = [ContextAnnotation(**ca) for ca in data['context_annotations']]
        
        if data.get('edit_controls'):
            data['edit_controls'] = EditControls(**data['edit_controls'])
        
        return cls(**data)


@dataclass
class FeedResponse:
    """
    Container for API-style feed responses with included expansions
    Similar to Twitter API v2 response structure
    """
    data: List[Feed]
    includes: Dict[str, Any] = field(default_factory=dict)  # users, media, polls, places
    meta: Dict[str, Any] = field(default_factory=dict)  # pagination, result count, etc.
    errors: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert FeedResponse to dictionary for JSON serialization"""
        return {
            "data": [feed.to_dict() for feed in self.data],
            "includes": self.includes,
            "meta": self.meta,
            "errors": self.errors if self.errors else None
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        data = self.to_dict()
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, indent=indent, ensure_ascii=False)
