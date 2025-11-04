import requests
from datetime import datetime
import sqlite3

# Token de integração do Notion
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'

# IDs das databases
CONTATOS_DB = '1f93392169d08196ab56f51082a83a45'
DEMANDAS_DB = '1f83392169d080aeb702ee337d1c2015'

def query_database_all(database_id):
    """Query database do Notion com paginação (pega todos os resultados)"""
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
        
        print(f"   Carregados {len(all_results)} registros...")
    
    return all_results

def collect_notion_stats():
    """Coleta estatísticas de contatos e demandas do Notion"""
    
    print("\n" + "="*60)
    print("📊 NOTION SCRAPER - Cris Monteiro")
    print("="*60 + "\n")
    
    try:
        # === CONTATOS (WhatsApp e Endereços) ===
        print("🔍 Consultando base de Contatos...")
        contatos_results = query_database_all(CONTATOS_DB)
        
        whatsapp_count = 0
        enderecos_count = 0
        
        for page in contatos_results:
            props = page['properties']
            
            # Conta celulares (WhatsApp) - título da página
            celular = props.get('Número de celular', {})
            if celular.get('title'):
                numeros = celular['title']
                if numeros and len(numeros) > 0 and numeros[0].get('plain_text', '').strip():
                    whatsapp_count += 1
            
            # Conta endereços preenchidos
            endereco_prop = props.get('Endereço', {})
            if endereco_prop.get('rich_text'):
                endereco = endereco_prop['rich_text']
                if endereco and len(endereco) > 0 and endereco[0].get('plain_text', '').strip():
                    enderecos_count += 1
        
        print(f"✅ WhatsApp: {whatsapp_count:,}")
        print(f"✅ Endereços: {enderecos_count:,}")
        
        # === DEMANDAS (Ofícios) ===
        print("\n🔍 Consultando base de Demandas...")
        demandas_results = query_database_all(DEMANDAS_DB)
        
        # Conta total de demandas (ofícios)
        oficios_count = len(demandas_results)
        
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
        print("="*60)
        print(f"📊 TOTAIS:")
        print(f"   📱 WhatsApp: {whatsapp_count:,}")
        print(f"   🏠 Endereços: {enderecos_count:,}")
        print(f"   📄 Ofícios: {oficios_count:,}")
        print("="*60 + "\n")
        
        return {
            'whatsapp': whatsapp_count, 
            'enderecos': enderecos_count,
            'oficios': oficios_count
        }
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    collect_notion_stats()
