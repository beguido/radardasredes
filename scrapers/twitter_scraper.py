#!/usr/bin/env python3
import os
import sqlite3
from apify_client import ApifyClient
from dotenv import load_dotenv

def init_db():
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS twitter_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            followers INTEGER,
            following INTEGER,
            tweets_count INTEGER,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def scrape_twitter(username='crismonteirosp'):
    load_dotenv()
    client = ApifyClient(os.environ.get('APIFY_TOKEN'))
    
    print(f"🐦 Coletando Twitter: @{username}")
    
    run_input = {
        "startUrls": [f"https://twitter.com/{username}"],
        "maxItems": 1,
        "maxTweetsPerQuery": 1
    }
    
    run = client.actor("61RPP7dywgiy0JPD0").call(run_input=run_input)
    
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # Pega dados do author (perfil)
        author = item.get('author', {})
        
        conn = sqlite3.connect('data/social_monitor.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO twitter_stats (username, followers, following, tweets_count) VALUES (?, ?, ?, ?)',
            (username, author.get('followers', 0), author.get('following', 0), author.get('statusesCount', 0))
        )
        conn.commit()
        conn.close()
        
        print(f"✅ {author.get('followers', 0):,} seguidores")
        return author
    
    print("❌ Sem dados")
    return None

if __name__ == '__main__':
    init_db()
    scrape_twitter()
