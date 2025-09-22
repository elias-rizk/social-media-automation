{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import json\
import requests\
import feedparser\
from datetime import datetime, timedelta\
import anthropic\
import random\
\
class TopicManager:\
    def __init__(self, config):\
        self.config = config\
        self.custom_topics = []\
        self.trending_topics = []\
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)\
        \
    def load_custom_topics(self, filename):\
        """Load your predefined topics of interest"""\
        try:\
            with open(filename, 'r') as f:\
                self.custom_topics = json.load(f)\
        except FileNotFoundError:\
            print(f"Custom topics file \{filename\} not found")\
            self.custom_topics = []\
    \
    def get_trending_topics(self):\
        """Fetch trending topics from various sources"""\
        trending = \{\
            'tech': self._get_tech_trends(),\
            'business': self._get_business_trends(),\
            'industry_specific': self._get_industry_trends()\
        \}\
        \
        self.trending_topics = trending\
        return trending\
    \
    def _get_tech_trends(self):\
        """Get tech trending topics from RSS feeds"""\
        feeds = [\
            'https://feeds.feedburner.com/oreilly/radar',\
            'https://techcrunch.com/feed/',\
            'https://www.wired.com/feed/category/business/latest/rss'\
        ]\
        \
        trends = []\
        for feed_url in feeds:\
            try:\
                feed = feedparser.parse(feed_url)\
                for entry in feed.entries[:5]:  # Top 5 from each source\
                    trends.append(\{\
                        'title': entry.title,\
                        'summary': entry.summary[:200] if hasattr(entry, 'summary') else '',\
                        'url': entry.link,\
                        'published': entry.published if hasattr(entry, 'published') else '',\
                        'source': feed_url\
                    \})\
            except Exception as e:\
                print(f"Error fetching from \{feed_url\}: \{e\}")\
        \
        return trends[:10]  # Return top 10 overall\
    \
    def _get_business_trends(self):\
        """Get business trending topics"""\
        feeds = [\
            'https://feeds.harvard.edu/news/rss/business',\
            'https://hbr.org/feed'\
        ]\
        trends = []\
        for feed_url in feeds:\
            try:\
                feed = feedparser.parse(feed_url)\
                for entry in feed.entries[:3]:\
                    trends.append(\{\
                        'title': entry.title,\
                        'summary': entry.summary[:200] if hasattr(entry, 'summary') else '',\
                        'url': entry.link\
                    \})\
            except Exception as e:\
                print(f"Error fetching from \{feed_url\}: \{e\}")\
        return trends\
    \
    def _get_industry_trends(self):\
        """Get industry-specific trends based on your field"""\
        return []\
    \
    def generate_topic_angles(self, topic):\
        """Generate different angles for a topic based on your voice"""\
        angles_prompt = f"""\
        Given this topic: \{topic\}\
        \
        Generate 3 different angles I could take when writing about this, considering:\
        1. My personal experience/perspective\
        2. Practical business implications\
        3. Future predictions/insights\
        \
        Each angle should be one sentence and reflect how I might uniquely approach this topic.\
        Return as JSON array of strings.\
        """\
        \
        try:\
            message = self.client.messages.create(\
                model="claude-3-sonnet-20240229",\
                max_tokens=500,\
                messages=[\{"role": "user", "content": angles_prompt\}]\
            )\
            \
            angles = json.loads(message.content[0].text)\
            return angles\
        except:\
            return [topic]  # Fallback to original topic\
    \
    def select_daily_topics(self, count=2):\
        """Select topics for today's posts"""\
        available_topics = []\
        \
        # Add custom topics\
        available_topics.extend(self.custom_topics)\
        \
        # Add trending topics with your angle\
        for category, trends in self.trending_topics.items():\
            for trend in trends:\
                angles = self.generate_topic_angles(trend['title'])\
                available_topics.extend(angles)\
        \
        # Randomly select topics (could be made smarter)\
        if len(available_topics) >= count:\
            selected = random.sample(available_topics, count)\
        else:\
            selected = available_topics\
            \
        return selected}