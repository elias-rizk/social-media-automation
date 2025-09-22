{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import anthropic\
import pandas as pd\
from textstat import flesch_reading_ease, flesch_kincaid_grade\
from sklearn.feature_extraction.text import TfidfVectorizer\
import re\
import json\
\
class VoiceAnalyzer:\
    def __init__(self, api_key):\
        self.client = anthropic.Anthropic(api_key=api_key)\
        self.voice_profile = \{\}\
        \
    def analyze_writing_samples(self, samples_file):\
        """Analyze your existing writing samples to extract voice patterns"""\
        with open(samples_file, 'r') as f:\
            samples = json.load(f)\
        \
        analysis = \{\
            'tone_patterns': self._analyze_tone(samples),\
            'vocabulary': self._analyze_vocabulary(samples),\
            'sentence_structure': self._analyze_structure(samples),\
            'topics_style': self._analyze_topic_approach(samples),\
            'engagement_style': self._analyze_engagement(samples)\
        \}\
        \
        self.voice_profile = analysis\
        return analysis\
    \
    def _analyze_tone(self, samples):\
        """Extract tone and emotional patterns"""\
        tone_prompt = f"""\
        Analyze these writing samples and identify the consistent tone patterns:\
        \
        \{' '.join(samples[:5])\}\
        \
        Return JSON with:\
        - primary_tone: (professional, casual, authoritative, etc.)\
        - emotional_range: (enthusiastic, measured, passionate, etc.)\
        - formality_level: (1-10 scale)\
        - humor_usage: (frequency and style)\
        """\
        \
        message = self.client.messages.create(\
            model="claude-3-sonnet-20240229",\
            max_tokens=1000,\
            messages=[\{"role": "user", "content": tone_prompt\}]\
        )\
        \
        try:\
            return json.loads(message.content[0].text)\
        except:\
            return \{\
                "primary_tone": "professional",\
                "emotional_range": "measured", \
                "formality_level": 7,\
                "humor_usage": "occasional"\
            \}\
    \
    def _analyze_vocabulary(self, samples):\
        """Analyze vocabulary patterns and word choices"""\
        all_text = ' '.join(samples)\
        \
        # Calculate readability\
        readability = \{\
            'flesch_score': flesch_reading_ease(all_text),\
            'grade_level': flesch_kincaid_grade(all_text)\
        \}\
        \
        # Extract common phrases and terms\
        vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=100)\
        tfidf_matrix = vectorizer.fit_transform(samples)\
        feature_names = vectorizer.get_feature_names_out()\
        \
        return \{\
            'readability': readability,\
            'common_terms': feature_names[:20].tolist(),\
            'avg_sentence_length': len(all_text.split()) / len(re.split(r'[.!?]', all_text))\
        \}\
    \
    def _analyze_structure(self, samples):\
        """Analyze sentence and paragraph structure"""\
        structures = []\
        for sample in samples:\
            sentences = re.split(r'[.!?]', sample)\
            structures.append(\{\
                'sentence_count': len([s for s in sentences if s.strip()]),\
                'avg_sentence_length': len(sample.split()) / len(sentences),\
                'question_usage': sample.count('?') / len(sentences),\
                'exclamation_usage': sample.count('!') / len(sentences)\
            \})\
        \
        return \{\
            'avg_sentence_count': sum(s['sentence_count'] for s in structures) / len(structures),\
            'avg_sentence_length': sum(s['avg_sentence_length'] for s in structures) / len(structures),\
            'question_frequency': sum(s['question_usage'] for s in structures) / len(structures),\
            'exclamation_frequency': sum(s['exclamation_usage'] for s in structures) / len(structures)\
        \}\
    \
    def _analyze_topic_approach(self, samples):\
        """Analyze how you approach different topics"""\
        return \{"approach": "analytical"\}\
    \
    def _analyze_engagement(self, samples):\
        """Analyze engagement patterns"""\
        return \{"engagement_style": "conversational"\}\
    \
    def generate_voice_prompt(self):\
        """Generate a prompt that captures your voice for content generation"""\
        return f"""\
        You are writing in my personal voice with these characteristics:\
        \
        TONE & STYLE:\
        - Primary tone: \{self.voice_profile['tone_patterns']['primary_tone']\}\
        - Formality level: \{self.voice_profile['tone_patterns']['formality_level']\}/10\
        - Emotional approach: \{self.voice_profile['tone_patterns']['emotional_range']\}\
        \
        WRITING PATTERNS:\
        - Average sentences per post: \{self.voice_profile['sentence_structure']['avg_sentence_count']\}\
        - Sentence length: \{self.voice_profile['sentence_structure']['avg_sentence_length']\} words\
        - Use questions \{self.voice_profile['sentence_structure']['question_frequency']*100:.1f\}% of the time\
        - Reading level: Grade \{self.voice_profile['vocabulary']['readability']['grade_level']\}\
        \
        VOCABULARY:\
        - Commonly use these terms: \{', '.join(self.voice_profile['vocabulary']['common_terms'][:10])\}\
        - Maintain readability score around \{self.voice_profile['vocabulary']['readability']['flesch_score']\}\
        \
        Write naturally as if I'm personally sharing my thoughts.\
        """}