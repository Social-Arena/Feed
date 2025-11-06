"""
Entity models for hashtags, mentions, and URLs in feed content
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional


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
        """Convert to dictionary"""
        return {
            "hashtags": [asdict(h) for h in self.hashtags],
            "mentions": [asdict(m) for m in self.mentions],
            "urls": [asdict(u) for u in self.urls]
        }

