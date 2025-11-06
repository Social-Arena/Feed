"""
Referenced feed models for replies, quotes, and retweets
"""

from dataclasses import dataclass
from enum import Enum


class ReferencedFeedType(Enum):
    """Types of references between feeds"""
    REPLIED_TO = "replied_to"
    QUOTED = "quoted"
    RETWEETED = "retweeted"


@dataclass
class ReferencedFeed:
    """Reference to another feed (reply, quote, retweet)"""
    type: str  # ReferencedFeedType value
    id: str

