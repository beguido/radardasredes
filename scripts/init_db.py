"""Inicializa banco de dados SQLite"""
import sqlite3
import os

DB_PATH = 'data/social_monitor.db'

# Cria pasta data se não existir
os.makedirs('data', exist_ok=True)

# Cria banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Tabela instagram_profiles
cursor.execute('''
    CREATE TABLE IF NOT EXISTS instagram_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        followers INTEGER,
        following INTEGER,
        posts_count INTEGER,
        avg_engagement_rate REAL,
        profile_picture_url TEXT,
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Tabela notion_stats
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notion_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        whatsapp INTEGER,
        enderecos INTEGER,
        oficios INTEGER,
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("✅ Banco inicializado!")
