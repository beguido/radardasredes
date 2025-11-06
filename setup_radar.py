#!/usr/bin/env python3
"""
SETUP - Radar das Redes
Inicializa o banco de dados e estrutura necessária
"""

import sqlite3
import os
from pathlib import Path

def criar_estrutura_pastas():
    """Cria pastas necessárias"""
    print("📁 Criando estrutura de pastas...")
    
    pastas = [
        'data',
        'assets',
        'assets/profile_photos',
        'scrapers',
        'scripts'
    ]
    
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {pasta}/")
    
    print()


def criar_tabela_radar_geral():
    """Cria tabela radar_geral no banco"""
    print("🗄️ Criando tabela radar_geral...")
    
    db_path = os.getenv('DATABASE_PATH', 'data/social_monitor.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabela principal
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS radar_geral (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            nome TEXT NOT NULL,
            cargo TEXT,
            partido TEXT,
            tier INTEGER,
            followers INTEGER,
            following INTEGER,
            posts_count INTEGER,
            avg_engagement_rate REAL,
            avg_likes REAL,
            avg_comments REAL,
            profile_picture_url TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, collected_at)
        )
    ''')
    
    # Índices
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_radar_username 
        ON radar_geral(username)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_radar_date 
        ON radar_geral(collected_at DESC)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_radar_tier 
        ON radar_geral(tier)
    ''')
    
    conn.commit()
    conn.close()
    
    print("  ✓ Tabela radar_geral criada")
    print("  ✓ Índices criados")
    print()


def verificar_tabela_instagram():
    """Verifica se a tabela do Instagram (Radar da Cris) existe"""
    print("🔍 Verificando tabela instagram_profiles...")
    
    db_path = os.getenv('DATABASE_PATH', 'data/social_monitor.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='instagram_profiles'
    ''')
    
    exists = cursor.fetchone() is not None
    conn.close()
    
    if exists:
        print("  ✓ Tabela instagram_profiles existe (Radar da Cris)")
    else:
        print("  ⚠️ Tabela instagram_profiles não existe")
        print("  ℹ️ Execute: python3 scripts/setup_database.py")
    
    print()
    return exists


def criar_env_exemplo():
    """Cria arquivo .env.example"""
    print("📝 Criando .env.example...")
    
    env_example = """# Configuração do Radar das Redes

# Token da Apify (obrigatório para scraping)
APIFY_API_TOKEN=seu_token_aqui

# Caminho do banco de dados
DATABASE_PATH=data/social_monitor.db

# Configuração do dashboard
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=8050
DASHBOARD_DEBUG=False

# Perfis do Radar da Cris (separados por vírgula)
INSTAGRAM_PROFILES=crismonteirosp,marinahelenabr,adriventurasp,leosiqueirabr
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_example)
    
    print("  ✓ .env.example criado")
    print()


def main():
    print("\n" + "="*60)
    print("🎯 SETUP - RADAR DAS REDES")
    print("="*60 + "\n")
    
    # Cria estrutura
    criar_estrutura_pastas()
    
    # Cria tabelas
    criar_tabela_radar_geral()
    
    # Verifica radar da Cris
    tem_cris = verificar_tabela_instagram()
    
    # Cria .env.example
    criar_env_exemplo()
    
    # Resumo
    print("="*60)
    print("✅ Setup completo!")
    print("="*60)
    print("\n📋 Próximos passos:\n")
    print("1. Configure seu .env com o token da Apify:")
    print("   cp .env.example .env")
    print("   # Edite .env e adicione seu token\n")
    
    if not tem_cris:
        print("2. Execute o setup do Radar da Cris:")
        print("   python3 scripts/setup_database.py\n")
    
    print("3. Colete dados iniciais:")
    print("   python3 scrapers/instagram_scraper.py  # Radar da Cris")
    print("   python3 scrapers/radargeral.py         # Radar Geral\n")
    
    print("4. Rode o dashboard:")
    print("   python3 scripts/run_social_monitor.py\n")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
