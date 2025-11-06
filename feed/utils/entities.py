"""
Entity extraction utilities for hashtags, mentions, and URLs
"""

import re
import hashlib
from typing import Optional

from ..models import Entities, HashtagEntity, MentionEntity, UrlEntity


def extract_entities(text: str) -> Optional[Entities]:
    """
    Extract entities (hashtags, mentions, URLs) from text
    
    Args:
        text: Text to extract entities from
        
    Returns:
        Entities object containing extracted entities, or None if no entities found
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
            id=hashlib.sha256(match.group(1).encode("utf-8")).hexdigest()[:16]
        ))
    
    # Extract URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    for match in re.finditer(url_pattern, text):
        url = match.group()
        entities.urls.append(UrlEntity(
            start=match.start(),
            end=match.end(),
            url=url,
            expanded_url=url,
            display_url=(
                (url.replace("https://", "").replace("http://", ""))
                if len(url.replace("https://", "").replace("http://", "")) <= 30
                else (url.replace("https://", "").replace("http://", ""))[:27] + "..."
            )
        ))
    
    return entities if (entities.hashtags or entities.mentions or entities.urls) else None

