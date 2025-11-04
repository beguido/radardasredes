#!/usr/bin/env python3
"""
TikTok Scraper usando Apify
Coleta métricas do perfil @crismonteirosp
"""

import os
import sqlite3
from datetime import datetime
from apify_client import ApifyClient

def init_db():
    """Cria tabela se não existir"""
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiktok_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            followers INTEGER,
            following INTEGER,
            likes INTEGER,
            videos_count INTEGER,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def scrape_tiktok(username='crismonteirosp'):
    """Scrape dados do TikTok usando Apify"""
    
    token = os.environ.get('APIFY_TOKEN')
    if not token:
        raise ValueError("APIFY_TOKEN não encontrado")
    
    client = ApifyClient(token)
    
    print(f"💃 Coletando dados do TikTok: @{username}")
    
    run_input = {
        "profiles": [f"@{username}"],
        "resultsPerPage": 1
    }
    
    run = client.actor("clockworks/tiktok-profile-scraper").call(run_input=run_input)
    
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)
    
    if not results:
        print("❌ Nenhum dado retornado")
        return None
    
    profile = results[0]
    
    # Salva no banco
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tiktok_stats (username, followers, following, likes, videos_count)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        username,
        profile.get('followerCount', 0),
        profile.get('followingCount', 0),
        profile.get('heartCount', 0),
        profile.get('videoCount', 0)
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ TikTok coletado: {profile.get('followerCount', 0):,} seguidores")
    
    return profile

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    init_db()
    scrape_tiktok()
