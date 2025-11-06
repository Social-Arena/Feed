"""
Content generation for Twitter simulation
"""

import random
from typing import List


class ContentGenerator:
    """Generate realistic Twitter content"""
    
    # Sample content templates
    TOPICS = {
        "technology": [
            "Just discovered {tech}! Game changer for {field} 🚀",
            "AI is revolutionizing {industry}. What are your thoughts? #AI #Tech",
            "New {product} release! Who's excited? 🎉 #{hashtag}",
            "Working on a {project} using {technology}. Stay tuned! 💻",
            "The future of {concept} is here! #Innovation",
        ],
        "news": [
            "BREAKING: {event} announced! More details to follow... 📰",
            "Just in: {organization} reports {finding}. #{news}",
            "Update on {situation}: {detail}",
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
            "Breaking: {athlete} signs with {team}! 📝",
            "That {play} though! Instant classic! 🏅 #{highlight}",
        ],
    }
    
    # Placeholder values for content generation
    PLACEHOLDERS = {
        "tech": ["Python", "React", "Kubernetes", "AI", "Blockchain"],
        "field": ["web development", "data science", "cybersecurity", "cloud computing"],
        "product": ["iPhone", "Framework", "API", "Tool", "Platform"],
        "project": ["ML model", "web app", "mobile app", "automation tool"],
        "technology": ["TensorFlow", "Docker", "GraphQL", "Rust", "WebAssembly"],
        "concept": ["metaverse", "Web3", "automation", "sustainability"],
        "event": ["Conference", "Summit", "Partnership", "Launch"],
        "organization": ["TechCorp", "Research Institute", "Startup"],
        "finding": ["breakthrough", "record growth", "new discovery"],
        "situation": ["market conditions", "policy change", "crisis"],
        "headline": ["Market hits all-time high", "New regulation passed"],
        "activity": ["coffee", "workout", "meditation", "reading"],
        "day": ["Monday", "Friday", "weekend", "month"],
        "accomplishment": ["workout", "project", "presentation"],
        "emotion": ["accomplished", "proud", "excited", "grateful"],
        "movie": ["The Latest Blockbuster", "Indie Film", "Classic Movie"],
        "show": ["Popular Series", "New Show", "Classic Sitcom"],
        "song": ["Top Hit", "New Release", "Classic Track"],
        "artist": ["Famous Singer", "Band Name", "DJ"],
        "game": ["Fortnite", "Among Us", "COD", "Minecraft"],
        "team": ["Home Team", "Favorites", "Underdogs"],
        "player": ["Star Player", "Rookie", "Veteran"],
        "athlete": ["Top Player", "Rising Star", "Legend"],
        "hashtag": ["Trending", "Viral", "MustSee", "Epic"],
    }
    
    @classmethod
    def generate_tweet(cls, topic: str = None) -> str:
        """Generate realistic tweet content based on topic"""
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
            count = random.randint(1, 3)
        
        hashtags = [
            "Trending", "Viral", "Tech", "Life", "Motivation",
            "Innovation", "Community", "Love", "Design", "Science",
        ]
        
        return random.sample(hashtags, min(count, len(hashtags)))
    
    @classmethod
    def generate_thread(cls, topic: str, length: int = 3) -> List[str]:
        """Generate content for a thread"""
        thread_content = []
        
        # Opening tweet
        thread_content.append(f"🧵 Thread: Let's talk about {topic} (1/{length})")
        
        # Middle tweets
        for i in range(2, length):
            content = cls.generate_tweet(topic.lower() if topic.lower() in cls.TOPICS else None)
            thread_content.append(f"{content} ({i}/{length})")
        
        # Closing tweet
        thread_content.append(f"That's all! Thoughts on {topic}? ({length}/{length})")
        
        return thread_content

