import os
import requests
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Token de integração do Notion
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_VERSION = '2022-06-28'

# IDs das databases
CONTATOS_DB = '1f93392169d08196ab56f51082a83a45'
DEMANDAS_DB = '1f83392169d080aeb702ee337d1c2015'

def query_database_all(database_id):
    """Query database do Notion com paginação"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    
    all_results = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        all_results.extend(data['results'])
        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')
    
    return all_results

def collect_notion_stats():
    """Coleta estatísticas de contatos e demandas do Notion"""
    
    print("\n" + "="*60)
    print("📊 NOTION SCRAPER - Cris Monteiro")
    print("="*60 + "\n")
    
    try:
        # === CONTATOS ===
        print("🔍 Consultando base de Contatos...")
        contatos = query_database_all(CONTATOS_DB)
        
        whatsapp_count = 0
        enderecos_count = 0
        
        for page in contatos:
            props = page['properties']
            
            # Conta celulares (título da página)
            if 'Número de celular' in props:
                title = props['Número de celular'].get('title', [])
                if title and len(title) > 0:
                    numero = title[0].get('plain_text', '').strip()
                    if numero:
                        whatsapp_count += 1
            
            # Conta endereços
            if 'Endereço' in props:
                endereco = props['Endereço'].get('rich_text', [])
                if endereco and len(endereco) > 0:
                    texto = endereco[0].get('plain_text', '').strip()
                    if texto:
                        enderecos_count += 1
        
        print(f"✅ WhatsApp: {whatsapp_count:,}")
        print(f"✅ Endereços: {enderecos_count:,}")
        
        # === DEMANDAS (Ofícios) ===
        print("\n🔍 Consultando base de Demandas...")
        demandas = query_database_all(DEMANDAS_DB)
        oficios_count = len(demandas)
        
        print(f"✅ Ofícios: {oficios_count:,}")
        
        # Salva no banco
        conn = sqlite3.connect('data/social_monitor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notion_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                whatsapp INTEGER,
                enderecos INTEGER,
                oficios INTEGER
            )
        ''')
        
        cursor.execute('''
            INSERT INTO notion_stats (whatsapp, enderecos, oficios)
            VALUES (?, ?, ?)
        ''', (whatsapp_count, enderecos_count, oficios_count))
        
        conn.commit()
        conn.close()
        
        print("\n💾 Dados salvos no banco!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    collect_notion_stats()
