"""
Main Twitter simulation orchestrator
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from ..models import Feed, FeedType, ReferencedFeed, ReferencedFeedType
from ..utils import FeedManager, extract_entities
from .config import SimulationConfig
from .behavior import UserBehavior
from .content import ContentGenerator
from .engagement import EngagementCalculator


class TwitterSimulator:
    """Main class for simulating Twitter activity"""
    
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
    
    def create_tweet(
        self,
        user: UserBehavior,
        timestamp: datetime,
        existing_tweets: List[Feed] = None
    ) -> Feed:
        """Create a single tweet by a user"""
        # Choose content topic based on user interests
        topic = random.choice(user.interests)
        content = ContentGenerator.generate_tweet(topic)
        
        # Add hashtags based on user behavior
        if random.random() < user.hashtag_usage_rate:
            hashtags = ContentGenerator.generate_hashtags(random.randint(1, 3))
            content += " " + " ".join(f"#{tag}" for tag in hashtags)
        
        # Add mentions based on user behavior
        if random.random() < user.mention_rate and self.users:
            mentioned_user = random.choice(self.users)
            content += f" @{mentioned_user.username}"
        
        # Add URLs based on user behavior
        if random.random() < user.url_share_rate:
            content += f" https://example.com/{topic.lower()}"
        
        # Determine feed type and references
        feed_type = FeedType.POST
        referenced_feeds = []
        conversation_id = None
        in_reply_to_user_id = None
        
        # Handle replies, quotes, retweets
        if existing_tweets and random.random() < self.config.reply_probability:
            # Reply to existing tweet
            referenced_tweet = random.choice(existing_tweets[-20:] if len(existing_tweets) > 20 else existing_tweets)
            feed_type = FeedType.REPLY
            conversation_id = referenced_tweet.conversation_id or referenced_tweet.id
            in_reply_to_user_id = referenced_tweet.author_id
            referenced_feeds = [
                ReferencedFeed(
                    type=ReferencedFeedType.REPLIED_TO.value,
                    id=referenced_tweet.id
                )
            ]
        elif existing_tweets and random.random() < self.config.quote_probability:
            # Quote tweet
            referenced_tweet = random.choice(existing_tweets[-20:] if len(existing_tweets) > 20 else existing_tweets)
            feed_type = FeedType.QUOTE
            referenced_feeds = [
                ReferencedFeed(
                    type=ReferencedFeedType.QUOTED.value,
                    id=referenced_tweet.id
                )
            ]
        
        # Create feed
        feed = self.manager.create_feed(
            text=content,
            author_id=user.user_id,
            feed_type=feed_type,
            created_at=timestamp.isoformat() + "Z",
            conversation_id=conversation_id,
            in_reply_to_user_id=in_reply_to_user_id,
            referenced_feeds=referenced_feeds
        )
        
        # Extract entities
        feed.entities = extract_entities(content)
        
        return feed
    
    def simulate(
        self,
        num_tweets: int = None,
        duration_hours: int = None
    ) -> Tuple[List[Feed], Dict[str, Any]]:
        """
        Simulate Twitter activity over a period of time.
        
        Returns:
            Tuple of (list of feeds, simulation statistics)
        """
        num_tweets = num_tweets or self.config.num_tweets
        duration_hours = duration_hours or self.config.duration_hours
        
        # Generate users if not already done
        if not self.users:
            self.generate_users()
        
        # Calculate time intervals
        start_time = datetime.utcnow() - timedelta(hours=duration_hours)
        time_interval = timedelta(hours=duration_hours) / num_tweets
        
        self.feeds = []
        stats = {
            "total_tweets": 0,
            "total_replies": 0,
            "total_quotes": 0,
            "total_retweets": 0,
            "total_engagement": 0,
            "by_hour": {},
            "viral_tweets": 0,
        }
        
        current_time = start_time
        
        for i in range(num_tweets):
            # Select user based on activity patterns (higher activity users tweet more)
            weights = [u.posting_frequency for u in self.users]
            user = random.choices(self.users, weights=weights)[0]
            
            # Create tweet
            feed = self.create_tweet(user, current_time, self.feeds)
            
            # Generate engagement metrics
            time_since_tweet = datetime.utcnow() - current_time
            engagement_score = EngagementCalculator.calculate_engagement_score(
                feed, user, time_since_tweet
            )
            
            initial_metrics = EngagementCalculator.generate_metrics(
                engagement_score, user.follower_count, self.config
            )
            
            # Simulate viral growth for some tweets
            if random.random() < 0.05:  # 5% chance of going viral
                feed.public_metrics = EngagementCalculator.simulate_viral_growth(
                    initial_metrics,
                    int(time_since_tweet.total_seconds() / 3600),
                    virality_factor=random.uniform(0.1, 0.3)
                )
                stats["viral_tweets"] += 1
            else:
                feed.public_metrics = initial_metrics
            
            self.feeds.append(feed)
            
            # Update statistics
            stats["total_tweets"] += 1
            stats["total_engagement"] += (
                feed.public_metrics.like_count +
                feed.public_metrics.retweet_count +
                feed.public_metrics.reply_count
            )
            
            if feed.referenced_feeds:
                for ref in feed.referenced_feeds:
                    if ref.type == ReferencedFeedType.REPLIED_TO.value:
                        stats["total_replies"] += 1
                    elif ref.type == ReferencedFeedType.QUOTED.value:
                        stats["total_quotes"] += 1
                    elif ref.type == ReferencedFeedType.RETWEETED.value:
                        stats["total_retweets"] += 1
            
            # Track by hour
            hour = current_time.hour
            stats["by_hour"][hour] = stats["by_hour"].get(hour, 0) + 1
            
            # Advance time
            current_time += time_interval
        
        return self.feeds, stats
    
    def save_results(self, save_individual: bool = True) -> Dict[str, Any]:
        """
        Save simulation results to files.
        
        Returns:
            Dictionary with paths to saved files and statistics
        """
        saved_files = []
        
        # Save individual tweets
        if save_individual:
            for feed in self.feeds:
                filepath = self.manager.save_feed(feed)
                saved_files.append(filepath)
        
        return {
            "saved_files": saved_files,
            "total_tweets": len(self.feeds),
            "total_users": len(self.users),
        }

