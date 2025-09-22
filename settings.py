{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
from dotenv import load_dotenv\
\
load_dotenv()\
\
class Config:\
    # API Configuration\
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')\
    \
    # LinkedIn Credentials\
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')\
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')\
    \
    # Twitter Credentials\
    TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')\
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')\
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')\
    \
    # Posting Configuration\
    POSTING_DAYS = os.getenv('POSTING_SCHEDULE', 'mon,wed,fri,sun').split(',')\
    POSTING_TIMES = os.getenv('POSTING_TIMES', '09:00,13:00,17:00').split(',')\
    \
    # Database\
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///social_media.db')\
    \
    # Content Settings\
    MIN_POST_INTERVAL_HOURS = 6\
    MAX_POSTS_PER_DAY = 2\
    \
    # Selenium Settings\
    HEADLESS_BROWSER = True\
    BROWSER_TIMEOUT = 30}