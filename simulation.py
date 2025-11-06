"""
Social Media Simulation Module
Tools for simulating social media activity and user behavior
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import json
import math

from .feed_models import (
    Feed, FeedType, FeedResponse, User, MediaItem,
    Poll, PollOption, PublicMetrics, ReferencedFeed,
    ReferencedFeedType, Attachments, GeoInfo, Place,
    ContextAnnotation
)
from .feed_utils import (
    FeedManager, extract_entities, create_sample_user,
    create_sample_media, create_thread
)


@dataclass
class SimulationConfig:
    """Configuration for social media simulation"""
    num_users: int = 100
    num_feeds: int = 1000
    duration_hours: int = 24
    platform: str = "generic"
    
    # Activity patterns
    peak_hours: List[int] = field(default_factory=lambda: [9, 12, 18, 21])  # Peak activity hours
    min_feeds_per_user: int = 1
    max_feeds_per_user: int = 10
    
    # Engagement rates (as percentages)
    like_rate: float = 0.15  # 15% chance of liking
    repost_rate: float = 0.03  # 3% chance of reposting
    reply_rate: float = 0.05  # 5% chance of replying
    quote_rate: float = 0.02  # 2% chance of quoting
    
    # Content distribution
    text_only_rate: float = 0.40  # 40% text only
    with_media_rate: float = 0.35  # 35% with media
    with_poll_rate: float = 0.05  # 5% with polls
    with_location_rate: float = 0.20  # 20% with location
    
    # Platform-specific settings
    platform_features: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserBehavior:
    """Model for simulating user behavior patterns"""
    user_id: str
    username: str
    activity_level: str  # "low", "medium", "high", "influencer"
    interests: List[str]
    posting_frequency: float  # Posts per hour
    engagement_probability: float
    follower_count: int
    following_count: int
    
    # Behavior patterns
    peak_activity_hours: List[int] = field(default_factory=list)
    preferred_feed_types: List[FeedType] = field(default_factory=list)
    hashtag_usage_rate: float = 0.3
    mention_rate: float = 0.2
    url_share_rate: float = 0.1
    
    def __post_init__(self):
        """Initialize behavior patterns based on activity level"""
        if self.activity_level == "low":
            self.posting_frequency = random.uniform(0.1, 0.3)
            self.engagement_probability = 0.1
            self.peak_activity_hours = random.sample(range(24), 2)
        elif self.activity_level == "medium":
            self.posting_frequency = random.uniform(0.3, 0.8)
            self.engagement_probability = 0.3
            self.peak_activity_hours = random.sample(range(24), 4)
        elif self.activity_level == "high":
            self.posting_frequency = random.uniform(0.8, 2.0)
            self.engagement_probability = 0.5
            self.peak_activity_hours = random.sample(range(24), 6)
        elif self.activity_level == "influencer":
            self.posting_frequency = random.uniform(2.0, 5.0)
            self.engagement_probability = 0.7
            self.peak_activity_hours = list(range(8, 23))  # Active most of the day


class ContentGenerator:
    """Generate realistic content for feeds"""
    
    # Sample content templates
    TOPICS = {
        "technology": [
            "Just discovered {tech}! Game changer for {field} 🚀",
            "AI is revolutionizing {industry}. What are your thoughts? #AI #Tech",
            "New {product} release! Who's excited? 🎉 #{hashtag}",
            "Working on a {project} using {technology}. Stay tuned! 💻",
            "The future of {concept} is here! Check out {link} #Innovation",
        ],
        "news": [
            "BREAKING: {event} announced! More details to follow... 📰",
            "Just in: {organization} reports {finding}. #{news}",
            "Update on {situation}: {detail} - via @{source}",
            "Important: {announcement} effective {date}. Please share!",
            "{headline}! What does this mean for {impact}? Discuss below 👇",
        ],
        "lifestyle": [
            "Good morning! Starting the day with {activity} ☀️ #{motivation}",
            "Can't believe it's already {day}! Time flies... ⏰",
            "Just finished {accomplishment}! Feeling {emotion} 💪",
            "Weekend vibes! Who else is {activity}? 🎉 #{weekend}",
            "Life hack: {tip}! You're welcome 😊 #{lifehack}",
        ],
        "entertainment": [
            "Just watched {movie}! {rating}/10 - Thoughts? 🎬 #{film}",
            "New episode of {show} was AMAZING! No spoilers but... 😱",
            "Currently listening to {song} on repeat 🎵 #{music}",
            "{artist} just dropped a new {content}! Stream it now! 🔥",
            "Gaming night! Who's playing {game}? 🎮 #{gaming}",
        ],
        "sports": [
            "What a game! {team} wins {score}! 🏆 #{sports}",
            "{player} with an incredible {achievement}! GOAT? 🐐",
            "Match day! Supporting {team} all the way! ⚽ #{matchday}",
            "Breaking: {athlete} signs with {team} for {amount}! 📝",
            "That {play} though! Instant classic! 🏅 #{highlight}",
        ],
    }
    
    # Placeholder values for content generation
    PLACEHOLDERS = {
        "tech": ["Python", "React", "Kubernetes", "Blockchain", "Quantum Computing"],
        "field": ["web development", "data science", "cybersecurity", "cloud computing"],
        "product": ["iPhone", "Framework", "API", "Tool", "Platform"],
        "project": ["machine learning model", "web app", "mobile app", "automation tool"],
        "technology": ["TensorFlow", "Docker", "GraphQL", "Rust", "WebAssembly"],
        "concept": ["metaverse", "Web3", "automation", "sustainability", "privacy"],
        "link": ["example.com/article", "bit.ly/demo", "github.com/project"],
        "event": ["Conference", "Summit", "Partnership", "Launch", "Acquisition"],
        "organization": ["TechCorp", "Research Institute", "Government", "Startup"],
        "finding": ["breakthrough", "record growth", "new discovery", "major update"],
        "situation": ["market conditions", "global event", "policy change", "crisis"],
        "headline": ["Market hits all-time high", "New regulation passed", "Discovery made"],
        "activity": ["coffee", "workout", "meditation", "reading", "coding"],
        "day": ["Monday", "Friday", "weekend", "month", "year"],
        "accomplishment": ["my workout", "the project", "the presentation", "cooking"],
        "emotion": ["accomplished", "proud", "exhausted", "excited", "grateful"],
        "movie": ["The Latest Blockbuster", "Indie Film", "Classic Movie", "Documentary"],
        "show": ["Popular Series", "New Show", "Classic Sitcom", "Reality Show"],
        "song": ["Top Hit", "New Release", "Classic Track", "Underground Beat"],
        "artist": ["Famous Singer", "Band Name", "DJ", "Producer"],
        "game": ["Fortnite", "Among Us", "COD", "Minecraft", "FIFA"],
        "team": ["Home Team", "Favorites", "Underdogs", "Champions"],
        "player": ["Star Player", "Rookie", "Veteran", "MVP"],
        "athlete": ["Top Player", "Rising Star", "Legend", "Prospect"],
        "hashtag": ["Trending", "Viral", "MustSee", "Epic", "Amazing"],
    }
    
    @classmethod
    def generate_content(cls, topic: str = None) -> str:
        """Generate realistic content based on topic"""
        if not topic:
            topic = random.choice(list(cls.TOPICS.keys()))
        
        templates = cls.TOPICS.get(topic, cls.TOPICS["lifestyle"])
        template = random.choice(templates)
        
        # Replace placeholders with values
        content = template
        for placeholder in cls.PLACEHOLDERS:
            if f"{{{placeholder}}}" in content:
                value = random.choice(cls.PLACEHOLDERS[placeholder])
                content = content.replace(f"{{{placeholder}}}", value)
        
        return content
    
    @classmethod
    def generate_hashtags(cls, count: int = None) -> List[str]:
        """Generate random hashtags"""
        if count is None:
            count = random.randint(1, 5)
        
        hashtags = [
            "Trending", "Viral", "MustSee", "Epic", "Amazing", "Breaking",
            "Innovation", "Tech", "Life", "Motivation", "Success", "Goals",
            "Community", "Love", "Art", "Design", "Photography", "Travel",
            "Food", "Fitness", "Health", "Mindfulness", "Nature", "Science",
        ]
        
        return random.sample(hashtags, min(count, len(hashtags)))
    
    @classmethod
    def generate_thread_content(cls, topic: str, length: int = 3) -> List[str]:
        """Generate content for a thread"""
        thread_content = []
        
        # Opening post
        thread_content.append(f"🧵 Thread: Let's talk about {topic} (1/{length})")
        
        # Middle posts
        for i in range(2, length):
            content = cls.generate_content(topic.lower() if topic.lower() in cls.TOPICS else None)
            thread_content.append(f"{content} ({i}/{length})")
        
        # Closing post
        thread_content.append(f"That's all for now! What are your thoughts on {topic}? ({length}/{length})")
        
        return thread_content


class EngagementSimulator:
    """Simulate engagement patterns and metrics"""
    
    @staticmethod
    def calculate_engagement_score(
        feed: Feed,
        author_behavior: UserBehavior,
        time_since_post: timedelta
    ) -> float:
        """
        Calculate engagement score based on various factors.
        Returns a score between 0 and 1.
        """
        score = 0.5  # Base score
        
        # Author influence factor
        if author_behavior.activity_level == "influencer":
            score += 0.2
        elif author_behavior.activity_level == "high":
            score += 0.1
        
        # Time decay factor (engagement decreases over time)
        hours_passed = time_since_post.total_seconds() / 3600
        time_factor = math.exp(-hours_passed / 24)  # Exponential decay over 24 hours
        score *= time_factor
        
        # Content type factor
        if feed.feed_type == FeedType.VIDEO:
            score += 0.15  # Videos get more engagement
        elif feed.feed_type == FeedType.IMAGE_POST:
            score += 0.1   # Images also perform well
        
        # Hashtag factor
        if feed.entities and feed.entities.hashtags:
            score += min(0.1, len(feed.entities.hashtags) * 0.02)
        
        return min(1.0, max(0.0, score))
    
    @staticmethod
    def generate_metrics(
        engagement_score: float,
        follower_count: int,
        config: SimulationConfig
    ) -> PublicMetrics:
        """Generate realistic metrics based on engagement score"""
        # Base reach (percentage of followers who see the post)
        reach = int(follower_count * engagement_score * random.uniform(0.1, 0.5))
        
        # Calculate metrics based on reach and config rates
        metrics = PublicMetrics(
            like_count=int(reach * config.like_rate * random.uniform(0.5, 1.5)),
            repost_count=int(reach * config.repost_rate * random.uniform(0.5, 1.5)),
            reply_count=int(reach * config.reply_rate * random.uniform(0.5, 1.5)),
            quote_count=int(reach * config.quote_rate * random.uniform(0.5, 1.5)),
            bookmark_count=int(reach * 0.01 * random.uniform(0.5, 1.5)),  # 1% bookmark rate
            impressions=reach * random.randint(2, 5),  # Multiple views per user
            view_count=reach * random.randint(1, 3) if random.random() < 0.3 else None,
            share_count=int(reach * 0.02 * random.uniform(0.5, 1.5)) if random.random() < 0.3 else None,
        )
        
        return metrics
    
    @staticmethod
    def simulate_viral_growth(
        initial_metrics: PublicMetrics,
        hours_elapsed: int,
        virality_factor: float = 0.1
    ) -> PublicMetrics:
        """Simulate viral growth pattern over time"""
        if random.random() > virality_factor:
            return initial_metrics  # Not going viral
        
        # Viral growth formula
        growth_factor = 1 + math.log(hours_elapsed + 1) * virality_factor
        
        return PublicMetrics(
            like_count=int(initial_metrics.like_count * growth_factor),
            repost_count=int(initial_metrics.repost_count * growth_factor * 1.5),  # Reposts drive virality
            reply_count=int(initial_metrics.reply_count * growth_factor * 0.8),
            quote_count=int(initial_metrics.quote_count * growth_factor * 1.2),
            bookmark_count=int(initial_metrics.bookmark_count * growth_factor * 0.6),
            impressions=int(initial_metrics.impressions * growth_factor * 2) if initial_metrics.impressions else None,
            view_count=int(initial_metrics.view_count * growth_factor * 1.8) if initial_metrics.view_count else None,
            share_count=int(initial_metrics.share_count * growth_factor * 1.3) if initial_metrics.share_count else None,
        )


class SocialSimulator:
    """Main class for simulating social media activity"""
    
    def __init__(self, config: SimulationConfig = None):
        """Initialize the simulator with configuration"""
        self.config = config or SimulationConfig()
        self.manager = FeedManager()
        self.users: List[UserBehavior] = []
        self.feeds: List[Feed] = []
        self.user_map: Dict[str, UserBehavior] = {}
        
    def generate_users(self, count: int = None) -> List[UserBehavior]:
        """Generate simulated users with varied behaviors"""
        count = count or self.config.num_users
        self.users = []
        
        # Distribution of user types
        distributions = {
            "influencer": int(count * 0.02),  # 2% influencers
            "high": int(count * 0.15),        # 15% high activity
            "medium": int(count * 0.50),      # 50% medium activity
            "low": int(count * 0.33),         # 33% low activity
        }
        
        user_id_counter = 1000
        
        for activity_level, num_users in distributions.items():
            for _ in range(num_users):
                user_id = str(user_id_counter)
                username = f"user_{user_id}"
                
                # Determine follower counts based on activity level
                if activity_level == "influencer":
                    follower_count = random.randint(10000, 1000000)
                    following_count = random.randint(100, 5000)
                elif activity_level == "high":
                    follower_count = random.randint(500, 10000)
                    following_count = random.randint(200, 2000)
                elif activity_level == "medium":
                    follower_count = random.randint(50, 500)
                    following_count = random.randint(50, 500)
                else:  # low
                    follower_count = random.randint(10, 100)
                    following_count = random.randint(20, 200)
                
                user = UserBehavior(
                    user_id=user_id,
                    username=username,
                    activity_level=activity_level,
                    interests=random.sample(list(ContentGenerator.TOPICS.keys()), random.randint(1, 3)),
                    posting_frequency=0,  # Set in __post_init__
                    engagement_probability=0,  # Set in __post_init__
                    follower_count=follower_count,
                    following_count=following_count,
                )
                
                self.users.append(user)
                self.user_map[user_id] = user
                user_id_counter += 1
        
        return self.users
    
    def simulate_feed_creation(
        self,
        user: UserBehavior,
        timestamp: datetime,
        existing_feeds: List[Feed] = None
    ) -> Feed:
        """Simulate creation of a single feed by a user"""
        # Choose content topic based on user interests
        topic = random.choice(user.interests)
        content = ContentGenerator.generate_content(topic)
        
        # Add hashtags based on user behavior
        if random.random() < user.hashtag_usage_rate:
            hashtags = ContentGenerator.generate_hashtags(random.randint(1, 3))
            content += " " + " ".join(f"#{tag}" for tag in hashtags)
        
        # Add mentions based on user behavior
        if random.random() < user.mention_rate and existing_feeds:
            mentioned_user = random.choice(self.users)
            content += f" @{mentioned_user.username}"
        
        # Add URLs based on user behavior
        if random.random() < user.url_share_rate:
            content += f" https://example.com/{topic.lower()}"
        
        # Determine feed type
        feed_type = FeedType.POST  # Default
        
        # Create feed
        feed = self.manager.create_feed(
            text=content,
            author_id=user.user_id,
            feed_type=feed_type,
            platform=self.config.platform,
            created_at=timestamp.isoformat() + "Z"
        )
        
        # Extract entities
        feed.entities = extract_entities(content)
        
        # Add media based on config
        if random.random() < self.config.with_media_rate:
            media_type = random.choice(["photo", "video"])
            media = create_sample_media(media_type)
            feed.attachments = Attachments(media_keys=[media.media_key])
            if media_type == "video":
                feed.feed_type = FeedType.VIDEO
        
        # Add location based on config
        if random.random() < self.config.with_location_rate:
            places = [
                ("New York, NY", "New York", 40.7128, -74.0060),
                ("Los Angeles, CA", "Los Angeles", 34.0522, -118.2437),
                ("London, UK", "London", 51.5074, -0.1278),
                ("Tokyo, Japan", "Tokyo", 35.6762, 139.6503),
                ("Paris, France", "Paris", 48.8566, 2.3522),
            ]
            place_data = random.choice(places)
            feed.geo = GeoInfo(
                place_id=f"place_{abs(hash(place_data[0]))}",
                coordinates={"type": "Point", "coordinates": [place_data[3], place_data[2]]}
            )
        
        # Simulate engagement (reference to existing feeds)
        if existing_feeds and random.random() < 0.2:  # 20% chance of referencing
            referenced_feed = random.choice(existing_feeds[-10:] if len(existing_feeds) > 10 else existing_feeds)
            
            if random.random() < 0.5:  # Reply
                feed.conversation_id = referenced_feed.conversation_id or referenced_feed.id
                feed.in_reply_to_user_id = referenced_feed.author_id
                feed.referenced_feeds = [
                    ReferencedFeed(
                        type=ReferencedFeedType.REPLIED_TO.value,
                        id=referenced_feed.id
                    )
                ]
            else:  # Quote
                feed.referenced_feeds = [
                    ReferencedFeed(
                        type=ReferencedFeedType.QUOTED.value,
                        id=referenced_feed.id
                    )
                ]
        
        return feed
    
    def simulate_activity(
        self,
        num_feeds: int = None,
        duration_hours: int = None
    ) -> Tuple[List[Feed], Dict[str, Any]]:
        """
        Simulate social media activity over a period of time.
        
        Returns:
            Tuple of (list of feeds, simulation statistics)
        """
        num_feeds = num_feeds or self.config.num_feeds
        duration_hours = duration_hours or self.config.duration_hours
        
        # Generate users if not already done
        if not self.users:
            self.generate_users()
        
        # Calculate time intervals
        start_time = datetime.utcnow() - timedelta(hours=duration_hours)
        time_interval = timedelta(hours=duration_hours) / num_feeds
        
        self.feeds = []
        stats = {
            "total_feeds": 0,
            "total_replies": 0,
            "total_quotes": 0,
            "total_media": 0,
            "total_engagement": 0,
            "by_platform": {},
            "by_type": {},
            "by_hour": {},
            "viral_feeds": 0,
        }
        
        current_time = start_time
        
        for i in range(num_feeds):
            # Select user based on activity patterns
            # Higher activity users post more frequently
            weights = [u.posting_frequency for u in self.users]
            user = random.choices(self.users, weights=weights)[0]
            
            # Create feed
            feed = self.simulate_feed_creation(user, current_time, self.feeds)
            
            # Generate initial metrics
            time_since_post = datetime.utcnow() - current_time
            engagement_score = EngagementSimulator.calculate_engagement_score(
                feed, user, time_since_post
            )
            
            initial_metrics = EngagementSimulator.generate_metrics(
                engagement_score, user.follower_count, self.config
            )
            
            # Simulate viral growth for some posts
            if random.random() < 0.05:  # 5% chance of going viral
                feed.public_metrics = EngagementSimulator.simulate_viral_growth(
                    initial_metrics,
                    int(time_since_post.total_seconds() / 3600),
                    virality_factor=random.uniform(0.1, 0.5)
                )
                stats["viral_feeds"] += 1
            else:
                feed.public_metrics = initial_metrics
            
            self.feeds.append(feed)
            
            # Update statistics
            stats["total_feeds"] += 1
            stats["total_engagement"] += (
                feed.public_metrics.like_count +
                feed.public_metrics.repost_count +
                feed.public_metrics.reply_count
            )
            
            if feed.referenced_feeds:
                for ref in feed.referenced_feeds:
                    if ref.type == ReferencedFeedType.REPLIED_TO.value:
                        stats["total_replies"] += 1
                    elif ref.type == ReferencedFeedType.QUOTED.value:
                        stats["total_quotes"] += 1
            
            if feed.attachments and feed.attachments.media_keys:
                stats["total_media"] += 1
            
            # Track by platform
            stats["by_platform"][feed.platform] = stats["by_platform"].get(feed.platform, 0) + 1
            
            # Track by type
            stats["by_type"][feed.feed_type.value] = stats["by_type"].get(feed.feed_type.value, 0) + 1
            
            # Track by hour
            hour = current_time.hour
            stats["by_hour"][hour] = stats["by_hour"].get(hour, 0) + 1
            
            # Advance time
            current_time += time_interval
        
        return self.feeds, stats
    
    def generate_sample_feeds(self, count: int = 10, platform: str = None) -> List[Feed]:
        """Generate sample feeds for testing"""
        if platform:
            self.config.platform = platform
        
        self.config.num_feeds = count
        feeds, _ = self.simulate_activity(num_feeds=count, duration_hours=24)
        return feeds
    
    def save_simulation(
        self,
        output_dir: str = "./simulation_output",
        save_individual: bool = True,
        save_response: bool = True
    ) -> Dict[str, Any]:
        """
        Save simulation results to files.
        
        Returns:
            Dictionary with paths to saved files and statistics
        """
        import os
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        saved_files = []
        
        # Save individual feeds
        if save_individual:
            for feed in self.feeds:
                filepath = self.manager.save_feed(feed)
                saved_files.append(filepath)
        
        # Save as response format
        if save_response:
            # Create user objects
            user_objects = []
            for user in self.users[:10]:  # Include first 10 users
                user_obj = User(
                    id=user.user_id,
                    username=user.username,
                    name=f"User {user.user_id}",
                    verified=user.activity_level == "influencer",
                    public_metrics={
                        "followers_count": user.follower_count,
                        "following_count": user.following_count,
                        "tweet_count": random.randint(100, 5000),
                        "listed_count": random.randint(0, 100)
                    }
                )
                user_objects.append(user_obj)
            
            response = FeedResponse(
                data=self.feeds[:100],  # Include first 100 feeds
                includes={
                    "users": [u.to_dict() for u in user_objects],
                    "media": [],
                    "places": [],
                },
                meta={
                    "result_count": len(self.feeds[:100]),
                    "total_count": len(self.feeds),
                    "simulation_config": {
                        "num_users": self.config.num_users,
                        "num_feeds": self.config.num_feeds,
                        "duration_hours": self.config.duration_hours,
                        "platform": self.config.platform,
                    }
                }
            )
            
            response_file = output_path / f"simulation-response-{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            with open(response_file, 'w', encoding='utf-8') as f:
                json.dump(response.to_dict(), f, indent=2, ensure_ascii=False)
            
            saved_files.append(str(response_file))
        
        return {
            "saved_files": saved_files,
            "total_feeds": len(self.feeds),
            "total_users": len(self.users),
            "output_directory": str(output_path)
        }
