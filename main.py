{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import sys\
import os\
sys.path.append(os.path.dirname(os.path.abspath(__file__)))\
\
from config.settings import Config\
from models.voice_analyzer import VoiceAnalyzer\
from agents.content_generator import ContentGenerator\
from agents.topic_manager import TopicManager\
from agents.scheduler import PostScheduler\
from utils.linkedin_connector import LinkedInConnector\
from utils.twitter_connector import TwitterConnector\
\
def initialize_voice_model():\
    """Initialize and train the voice model"""\
    print("Initializing voice analyzer...")\
    voice_analyzer = VoiceAnalyzer(Config.ANTHROPIC_API_KEY)\
    \
    # Load and analyze your writing samples\
    try:\
        analysis = voice_analyzer.analyze_writing_samples('data/training/voice_samples.json')\
        print("Voice analysis completed:")\
        print(f"- Primary tone: \{analysis['tone_patterns']['primary_tone']\}")\
        print(f"- Formality level: \{analysis['tone_patterns']['formality_level']\}/10")\
        print(f"- Average sentence length: \{analysis['sentence_structure']['avg_sentence_length']:.1f\} words")\
        return voice_analyzer\
    except FileNotFoundError:\
        print("Voice samples not found. Please create data/training/voice_samples.json first.")\
        return None\
\
def main():\
    print("=== Social Media Automation Tool ===")\
    \
    # Initialize components\
    voice_analyzer = initialize_voice_model()\
    if not voice_analyzer:\
        return\
    \
    content_generator = ContentGenerator(voice_analyzer, Config)\
    topic_manager = TopicManager(Config)\
    \
    # Load custom topics\
    try:\
        topic_manager.load_custom_topics('data/topics/custom_topics.json')\
        print(f"Loaded \{len(topic_manager.custom_topics)\} custom topics")\
    except FileNotFoundError:\
        print("Custom topics file not found. Using trending topics only.")\
    \
    # Initialize social media connectors\
    linkedin_connector = LinkedInConnector(\
        Config.LINKEDIN_EMAIL, \
        Config.LINKEDIN_PASSWORD,\
        headless=Config.HEADLESS_BROWSER\
    )\
    \
    twitter_connector = TwitterConnector(\
        Config.TWITTER_EMAIL,\
        Config.TWITTER_PASSWORD, \
        Config.TWITTER_USERNAME,\
        headless=Config.HEADLESS_BROWSER\
    )\
    \
    # Test connections\
    print("Testing social media connections...")\
    linkedin_success = linkedin_connector.login()\
    twitter_success = twitter_connector.login()\
    \
    if linkedin_success:\
        print("\uc0\u10003  LinkedIn connection successful")\
    else:\
        print("\uc0\u10007  LinkedIn connection failed")\
    \
    if twitter_success:\
        print("\uc0\u10003  Twitter connection successful")  \
    else:\
        print("\uc0\u10007  Twitter connection failed")\
    \
    if not (linkedin_success or twitter_success):\
        print("No social media connections available. Exiting.")\
        return\
    \
    # Initialize scheduler\
    scheduler = PostScheduler(\
        Config, content_generator, topic_manager, \
        linkedin_connector, twitter_connector\
    )\
    \
    # Start the scheduler\
    print(f"Starting scheduler for \{Config.POSTING_DAYS\} at \{Config.POSTING_TIMES\}")\
    try:\
        scheduler.run_scheduler()\
    except KeyboardInterrupt:\
        print("\\nShutting down scheduler...")\
        linkedin_connector.close()\
        twitter_connector.close()\
        print("Goodbye!")\
\
if __name__ == "__main__":\
    main()}