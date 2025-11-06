"""
Public engagement metrics for feeds
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PublicMetrics:
    """Public engagement metrics for a feed"""
    retweet_count: int = 0
    reply_count: int = 0
    like_count: int = 0
    quote_count: int = 0
    bookmark_count: int = 0
    impression_count: Optional[int] = None

