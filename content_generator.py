{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import anthropic\
import json\
from datetime import datetime\
import random\
\
class ContentGenerator:\
    def __init__(self, voice_analyzer, config):\
        self.voice_analyzer = voice_analyzer\
        self.config = config\
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)\
        \
    def generate_post(self, topic, platform, trending_context=None):\
        """Generate a post in your voice for specific platform"""\
        \
        platform_specs = \{\
            'linkedin': \{\
                'max_length': 1300,\
                'style': 'professional networking',\
                'hashtags': '3-5',\
                'call_to_action': True\
            \},\
            'twitter': \{\
                'max_length': 280,\
                'style': 'concise and engaging',\
                'hashtags': '1-2',\
                'thread_option': True\
            \}\
        \}\
        \
        spec = platform_specs[platform]\
        voice_prompt = self.voice_analyzer.generate_voice_prompt()\
        \
        content_prompt = f"""\
        \{voice_prompt\}\
        \
        TASK: Write a \{platform\} post about: \{topic\}\
        \
        PLATFORM REQUIREMENTS:\
        - Maximum \{spec['max_length']\} characters\
        - Style: \{spec['style']\}\
        - Include \{spec['hashtags']\} relevant hashtags\
        - \{'Include a call-to-action' if spec.get('call_to_action') else ''\}\
        \
        TRENDING CONTEXT:\
        \{trending_context if trending_context else 'No specific trending context'\}\
        \
        TOPIC FOCUS: \{topic\}\
        \
        Write the post exactly as I would, maintaining my authentic voice and perspective.\
        Return only the post content, no additional commentary.\
        """\
        \
        message = self.client.messages.create(\
            model="claude-3-sonnet-20240229",\
            max_tokens=500,\
            messages=[\{"role": "user", "content": content_prompt\}]\
        )\
        \
        return message.content[0].text.strip()\
    \
    def generate_thread(self, topic, max_tweets=5):\
        """Generate a Twitter thread"""\
        thread_prompt = f"""\
        \{self.voice_analyzer.generate_voice_prompt()\}\
        \
        Create a Twitter thread about: \{topic\}\
        \
        Requirements:\
        - \{max_tweets\} tweets maximum\
        - Each tweet under 280 characters\
        - Connected narrative flow\
        - End with engagement question\
        - Include relevant hashtags in last tweet\
        \
        Format as numbered list:\
        1. [First tweet]\
        2. [Second tweet]\
        etc.\
        """\
        \
        message = self.client.messages.create(\
            model="claude-3-sonnet-20240229",\
            max_tokens=1000,\
            messages=[\{"role": "user", "content": thread_prompt\}]\
        )\
        \
        thread_text = message.content[0].text.strip()\
        tweets = []\
        \
        for line in thread_text.split('\\n'):\
            if line.strip() and line[0].isdigit():\
                tweet = line.split('.', 1)[1].strip()\
                if len(tweet) <= 280:\
                    tweets.append(tweet)\
        \
        return tweets}