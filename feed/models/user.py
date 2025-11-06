"""
User model for Twitter simulation
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Optional


@dataclass
class User:
    """Twitter user information"""
    id: str
    username: str
    name: str
    profile_image_url: Optional[str] = None
    verified: bool = False
    description: Optional[str] = None
    created_at: Optional[str] = None
    public_metrics: Optional[Dict[str, int]] = None  # followers_count, following_count, etc.
    location: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert User to dictionary for JSON serialization"""
        return asdict(self)

