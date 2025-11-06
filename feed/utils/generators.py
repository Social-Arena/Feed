"""
Generator utilities for creating IDs and sample data
"""

import random
import string
from datetime import datetime
from typing import Optional

from ..models import User


def generate_feed_id(prefix: str = "") -> str:
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

