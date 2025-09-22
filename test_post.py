{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """Test script to generate and preview posts without actually posting"""\
\
from main import initialize_voice_model, Config\
from agents.content_generator import ContentGenerator\
from agents.topic_manager import TopicManager\
\
def test_content_generation():\
    """Test content generation without posting"""\
    \
    voice_analyzer = initialize_voice_model()\
    if not voice_analyzer:\
        return\
    \
    content_generator = ContentGenerator(voice_analyzer, Config)\
    topic_manager = TopicManager(Config)\
    \
    # Load topics\
    topic_manager.load_custom_topics('data/topics/custom_topics.json')\
    topic_manager.get_trending_topics()\
    \
    # Get a test topic\
    topics = topic_manager.select_daily_topics(count=1)\
    topic = topics[0] if topics else "The future of AI in business"\
    \
    print(f"\\n=== Testing Content Generation ===")\
    print(f"Topic: \{topic\}\\n")\
    \
    # Generate LinkedIn post\
    print("LinkedIn Post:")\
    print("-" * 50)\
    linkedin_post = content_generator.generate_post(topic, 'linkedin')\
    print(linkedin_post)\
    print(f"\\nLength: \{len(linkedin_post)\} characters")\
    \
    print("\\n" + "="*60 + "\\n")\
    \
    # Generate Twitter post\
    print("Twitter Post:")\
    print("-" * 50)\
    twitter_post = content_generator.generate_post(topic, 'twitter')\
    print(twitter_post)\
    print(f"\\nLength: \{len(twitter_post)\} characters")\
    \
    print("\\n" + "="*60 + "\\n")\
    \
    # Generate Twitter thread\
    print("Twitter Thread:")\
    print("-" * 50)\
    thread = content_generator.generate_thread(topic)\
    for i, tweet in enumerate(thread, 1):\
        print(f"\{i\}. \{tweet\}")\
        print(f"   Length: \{len(tweet)\} characters")\
        print()\
\
if __name__ == "__main__":\
    test_content_generation()}