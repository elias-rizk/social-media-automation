{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, render_template, jsonify, request\
import sqlite3\
from datetime import datetime, timedelta\
import json\
\
app = Flask(__name__, template_folder='../templates')\
\
def get_db_connection():\
    conn = sqlite3.connect('social_media.db')\
    conn.row_factory = sqlite3.Row\
    return conn\
\
@app.route('/')\
def dashboard():\
    """Main dashboard"""\
    conn = get_db_connection()\
    \
    # Recent posts\
    recent_posts = conn.execute('''\
        SELECT * FROM posts \
        ORDER BY scheduled_time DESC \
        LIMIT 10\
    ''').fetchall()\
    \
    # Stats for last 7 days\
    stats = conn.execute('''\
        SELECT \
            platform,\
            COUNT(*) as total_posts,\
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_posts\
        FROM posts \
        WHERE scheduled_time > datetime('now', '-7 days')\
        GROUP BY platform\
    ''').fetchall()\
    \
    conn.close()\
    \
    return render_template('dashboard.html', posts=recent_posts, stats=stats)\
\
@app.route('/api/posts')\
def get_posts():\
    """API endpoint for posts data"""\
    conn = get_db_connection()\
    posts = conn.execute('''\
        SELECT * FROM posts \
        ORDER BY scheduled_time DESC \
        LIMIT 50\
    ''').fetchall()\
    conn.close()\
    \
    return jsonify([dict(post) for post in posts])\
\
if __name__ == '__main__':\
    app.run(debug=True, port=5000)}