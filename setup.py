{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
\
import os\
import json\
import subprocess\
import sys\
\
def create_directory_structure():\
    """Create necessary directories"""\
    directories = [\
        'src/agents', 'src/models', 'src/utils', 'src/config',\
        'data/training', 'data/topics', 'data/posts',\
        'templates', 'logs', 'tests'\
    ]\
    \
    for directory in directories:\
        os.makedirs(directory, exist_ok=True)\
        print(f"\uc0\u10003  Created directory: \{directory\}")\
\
def install_dependencies():\
    """Install Python dependencies"""\
    try:\
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])\
        print("\uc0\u10003  Dependencies installed successfully")\
    except subprocess.CalledProcessError:\
        print("\uc0\u10007  Failed to install dependencies")\
        return False\
    return True\
\
def create_sample_files():\
    """Create sample configuration files if they don't exist"""\
    \
    # Sample voice training data\
    voice_file = 'data/training/voice_samples.json'\
    if not os.path.exists(voice_file):\
        sample_posts = [\
            "Just finished reading about the latest developments in machine learning. The practical applications in business are becoming more impressive every day.",\
            "Hot take: The best leaders aren't the ones who have all the answers - they're the ones who ask the right questions.",\
            "Reflecting on team dynamics today. It's amazing how much clarity comes from simply listening more than talking.",\
        ]\
        \
        os.makedirs(os.path.dirname(voice_file), exist_ok=True)\
        with open(voice_file, 'w') as f:\
            json.dump(sample_posts, f, indent=2)\
        print(f"\uc0\u10003  Created \{voice_file\}")\
    \
    # Sample topics\
    topics_file = 'data/topics/custom_topics.json'\
    if not os.path.exists(topics_file):\
        topics = [\
            "The future of remote work",\
            "AI ethics in business decisions", \
            "Building resilient teams",\
            "Innovation vs. execution balance"\
        ]\
        \
        os.makedirs(os.path.dirname(topics_file), exist_ok=True)\
        with open(topics_file, 'w') as f:\
            json.dump(topics, f, indent=2)\
        print(f"\uc0\u10003  Created \{topics_file\}")\
    \
    # Sample .env file\
    if not os.path.exists('.env.example'):\
        env_template = """# API Keys (Replace with your actual keys)\
ANTHROPIC_API_KEY=your_anthropic_api_key_here\
\
# LinkedIn Credentials\
LINKEDIN_EMAIL=your_linkedin_email\
LINKEDIN_PASSWORD=your_linkedin_password\
\
# Twitter Credentials  \
TWITTER_EMAIL=your_twitter_email\
TWITTER_PASSWORD=your_twitter_password\
TWITTER_USERNAME=your_twitter_username\
\
# Posting Configuration\
POSTING_SCHEDULE=mon,wed,fri,sun\
POSTING_TIMES=09:00,13:00,17:00\
DATABASE_URL=sqlite:///social_media.db\
"""\
        \
        with open('.env.example', 'w') as f:\
            f.write(env_template)\
        print("\uc0\u10003  Created .env.example file")\
\
def main():\
    print("=== Social Media Automation Setup ===\\n")\
    \
    print("1. Creating directory structure...")\
    create_directory_structure()\
    \
    print("\\n2. Installing dependencies...")\
    if not install_dependencies():\
        return\
    \
    print("\\n3. Creating sample files...")\
    create_sample_files()\
    \
    print("\\n=== Setup Complete! ===")\
    print("\\nNext steps:")\
    print("1. Copy .env.example to .env and add your actual credentials")\
    print("2. Add your writing samples to data/training/voice_samples.json")\
    print("3. Customize topics in data/topics/custom_topics.json")  \
    print("4. Run 'python src/test_post.py' to test content generation")\
    print("5. Run 'python src/main.py' to start the automation")\
    print("6. Run 'python src/dashboard.py' to view the web dashboard")\
\
if __name__ == "__main__":\
    main()}