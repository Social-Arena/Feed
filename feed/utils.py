"""Twitter Feed utilities"""

import json
import re
import hashlib
from datetime import datetime
from typing import Optional
from pathlib import Path

from .models import Feed, Entities, HashtagEntity, MentionEntity, UrlEntity


def generate_feed_id() -> str:
    """Generate unique feed ID from timestamp"""
    return str(int(datetime.utcnow().timestamp() * 1000000))


def extract_entities(text: str) -> Optional[Entities]:
    """Extract hashtags, mentions, URLs from text"""
    entities = Entities()
    
    for match in re.finditer(r'#(\w+)', text):
        entities.hashtags.append(HashtagEntity(
            start=match.start(), end=match.end(), tag=match.group(1)
        ))
    
    for match in re.finditer(r'@(\w+)', text):
        entities.mentions.append(MentionEntity(
            start=match.start(), end=match.end(), username=match.group(1),
            id=hashlib.sha256(match.group(1).encode()).hexdigest()[:16]
        ))
    
    for match in re.finditer(r'https?://[^\s<>"{}|\\^`\[\]]+', text):
        url = match.group()
        display = url.replace("https://", "").replace("http://", "")
        entities.urls.append(UrlEntity(
            start=match.start(), end=match.end(), url=url, expanded_url=url,
            display_url=display if len(display) <= 30 else display[:27] + "..."
        ))
    
    return entities if (entities.hashtags or entities.mentions or entities.urls) else None


def save_feed(feed: Feed, filepath: str) -> str:
    """Save feed to JSON file"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(feed.to_dict(), f, indent=2, ensure_ascii=False)
    return str(path.absolute())


def load_feed(filepath: str) -> Feed:
    """Load feed from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return Feed.from_dict(json.load(f))
