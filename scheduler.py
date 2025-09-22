{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import schedule\
import time\
import random\
from datetime import datetime, timedelta\
import json\
import sqlite3\
\
class PostScheduler:\
    def __init__(self, config, content_generator, topic_manager, linkedin_connector, twitter_connector):\
        self.config = config\
        self.content_generator = content_generator\
        self.topic_manager = topic_manager\
        self.linkedin_connector = linkedin_connector\
        self.twitter_connector = twitter_connector\
        self.db_path = config.DATABASE_URL.replace('sqlite:///', '')\
        self.setup_database()\
    \
    def setup_database(self):\
        """Initialize SQLite database for tracking posts"""\
        conn = sqlite3.connect(self.db_path)\
        cursor = conn.cursor()\
        \
        cursor.execute('''\
            CREATE TABLE IF NOT EXISTS posts (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                platform TEXT NOT NULL,\
                content TEXT NOT NULL,\
                topic TEXT,\
                post_id TEXT,\
                scheduled_time TEXT,\
                posted_time TEXT,\
                status TEXT,\
                engagement_metrics TEXT\
            )\
        ''')\
        \
        conn.commit()\
        conn.close()\
    \
    def schedule_posts(self):\
        """Set up the posting schedule"""\
        # Clear existing schedule\
        schedule.clear()\
        \
        # Schedule for each day and time combination\
        for day in self.config.POSTING_DAYS:\
            for time_slot in self.config.POSTING_TIMES:\
                getattr(schedule.every(), day.lower()).at(time_slot).do(self.create_and_post)\
        \
        print(f"Scheduled posts for \{self.config.POSTING_DAYS\} at \{self.config.POSTING_TIMES\}")\
    \
    def create_and_post(self):\
        """Main function to create and post content"""\
        if not self.should_post_now():\
            print("Skipping post - too soon since last post")\
            return\
        \
        # Get fresh trending topics\
        self.topic_manager.get_trending_topics()\
        \
        # Select topic for today\
        topics = self.topic_manager.select_daily_topics(count=1)\
        if not topics:\
            print("No topics available for posting")\
            return\
        \
        topic = topics[0]\
        print(f"Selected topic: \{topic\}")\
        \
        # Decide platform(s) - could be both or alternating\
        platforms = self.select_platforms()\
        \
        for platform in platforms:\
            try:\
                # Generate content\
                if platform == 'twitter' and random.random() < 0.3:  # 30% chance of thread\
                    content = self.content_generator.generate_thread(topic)\
                    result = self.twitter_connector.post_thread(content)\
                    content_text = ' | '.join(content)  # Store as joined string\
                else:\
                    content = self.content_generator.generate_post(topic, platform)\
                    \
                    if platform == 'linkedin':\
                        result = self.linkedin_connector.post_update(content)\
                    else:  # twitter\
                        result = self.twitter_connector.post_tweet(content)\
                    \
                    content_text = content\
                \
                # Log the post\
                self.log_post(platform, content_text, topic, result)\
                \
                if result.get('success'):\
                    print(f"Successfully posted to \{platform\}")\
                else:\
                    print(f"Failed to post to \{platform\}: \{result.get('error')\}")\
                \
            except Exception as e:\
                print(f"Error posting to \{platform\}: \{e\}")\
    \
    def should_post_now(self):\
        """Check if enough time has passed since last post"""\
        conn = sqlite3.connect(self.db_path)\
        cursor = conn.cursor()\
        \
        cursor.execute('''\
            SELECT MAX(posted_time) FROM posts \
            WHERE posted_time IS NOT NULL AND status = 'success'\
        ''')\
        \
        last_post = cursor.fetchone()[0]\
        conn.close()\
        \
        if not last_post:\
            return True\
        \
        last_post_time = datetime.fromisoformat(last_post)\
        time_diff = datetime.now() - last_post_time\
        \
        return time_diff.total_seconds() > (self.config.MIN_POST_INTERVAL_HOURS * 3600)\
    \
    def select_platforms(self):\
        """Decide which platform(s) to post to"""\
        # Simple logic - could be made more sophisticated\
        platforms = ['linkedin', 'twitter']\
        \
        # Check recent posts to ensure balance\
        conn = sqlite3.connect(self.db_path)\
        cursor = conn.cursor()\
        \
        cursor.execute('''\
            SELECT platform, COUNT(*) as count FROM posts \
            WHERE posted_time > datetime('now', '-7 days')\
            GROUP BY platform\
        ''')\
        \
        recent_counts = dict(cursor.fetchall())\
        conn.close()\
        \
        # Favor platform with fewer recent posts\
        linkedin_count = recent_counts.get('linkedin', 0)\
        twitter_count = recent_counts.get('twitter', 0)\
        \
        if linkedin_count < twitter_count:\
            return ['linkedin']\
        elif twitter_count < linkedin_count:\
            return ['twitter']\
        else:\
            return [random.choice(platforms)]\
    \
    def log_post(self, platform, content, topic, result):\
        """Log post attempt to database"""\
        conn = sqlite3.connect(self.db_path)\
        cursor = conn.cursor()\
        \
        status = 'success' if result.get('success') else 'failed'\
        post_id = result.get('post_id')\
        \
        cursor.execute('''\
            INSERT INTO posts (platform, content, topic, post_id, scheduled_time, posted_time, status)\
            VALUES (?, ?, ?, ?, ?, ?, ?)\
        ''', (\
            platform,\
            content[:500],  # Truncate for storage\
            topic,\
            post_id,\
            datetime.now().isoformat(),\
            datetime.now().isoformat() if result.get('success') else None,\
            status\
        ))\
        \
        conn.commit()\
        conn.close()\
    \
    def run_scheduler(self):\
        """Start the scheduler loop"""\
        print("Starting social media scheduler...")\
        self.schedule_posts()\
        \
        while True:\
            schedule.run_pending()\
            time.sleep(60)  # Check every minute}