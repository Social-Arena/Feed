"""Twitter Feed data models powered by Pydantic"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FeedType(str, Enum):
    POST = "post"
    REPLY = "reply"
    QUOTE = "quote"
    RETWEET = "retweet"
    THREAD = "thread"


class ReferencedFeedType(str, Enum):
    REPLIED_TO = "replied_to"
    QUOTED = "quoted"
    RETWEETED = "retweeted"


class HashtagEntity(BaseModel):
    start: int
    end: int
    tag: str


class MentionEntity(BaseModel):
    start: int
    end: int
    username: str
    id: str


class UrlEntity(BaseModel):
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str


class Entities(BaseModel):
    hashtags: List[HashtagEntity] = Field(default_factory=list)
    mentions: List[MentionEntity] = Field(default_factory=list)
    urls: List[UrlEntity] = Field(default_factory=list)


class PublicMetrics(BaseModel):
    retweet_count: int = 0
    reply_count: int = 0
    like_count: int = 0
    quote_count: int = 0
    bookmark_count: int = 0
    impression_count: Optional[int] = None


class ReferencedFeed(BaseModel):
    type: ReferencedFeedType
    id: str


class User(BaseModel):
    id: str
    username: str
    name: str
    verified: bool = False
    description: Optional[str] = None
    public_metrics: Optional[Dict[str, int]] = None


class Feed(BaseModel):
    """Main Twitter Feed data structure"""

    model_config = ConfigDict(use_enum_values=True)

    id: str
    text: str
    author_id: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    feed_type: FeedType = FeedType.POST
    conversation_id: Optional[str] = None
    in_reply_to_user_id: Optional[str] = None
    referenced_feeds: List[ReferencedFeed] = Field(default_factory=list)
    entities: Optional[Entities] = None
    public_metrics: PublicMetrics = Field(default_factory=PublicMetrics)

    @model_validator(mode="after")
    def ensure_conversation_id(self) -> "Feed":
        if self.conversation_id is None:
            self.conversation_id = self.id
        return self

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Feed":
        return cls(**data)
