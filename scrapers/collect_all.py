#!/usr/bin/env python3
"""
Script Mestre de Coleta de Dados
Coleta automaticamente o que tem scraper e pede input para o resto
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def collect_instagram():
    """Coleta Instagram via Apify"""
    print("📸 Coletando Instagram...")
    try:
        from instagram_scraper import scrape_instagram_profiles
        scrape_instagram_profiles()
        print("✅ Instagram coletado!")
        return True
    except Exception as e:
        print(f"❌ Erro no Instagram: {e}")
        return False

def collect_notion():
    """Coleta WhatsApp, Endereços, Ofícios via Notion"""
    print("📋 Coletando dados do Notion (WhatsApp, Endereços, Ofícios)...")
    try:
        from notion_scraper import scrape_notion
        scrape_notion()
        print("✅ Notion coletado!")
        return True
    except Exception as e:
        print(f"❌ Erro no Notion: {e}")
        return False

def collect_manual_social():
    """Coleta manual das redes sociais sem scraper"""
    import sqlite3
    
    print_header("REDES SOCIAIS - Entrada Manual")
    
    social_networks = {
        'Twitter': {'table': 'twitter_stats', 'fields': ['followers', 'following', 'tweets_count']},
        'TikTok': {'table': 'tiktok_stats', 'fields': ['followers', 'following', 'likes', 'videos_count']},
        'YouTube': {'table': 'youtube_stats', 'fields': ['subscribers', 'views', 'videos_count']},
        'Facebook': {'table': 'facebook_stats', 'fields': ['followers', 'likes', 'posts_count']},
        'LinkedIn': {'table': 'linkedin_stats', 'fields': ['connections', 'followers']},
        'Email': {'table': 'email_stats', 'fields': ['subscribers', 'active_rate']}
    }
    
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    
    # Cria tabelas se não existirem
    for network, config in social_networks.items():
        table = config['table']
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT DEFAULT 'crismonteirosp',
                {', '.join([f'{field} INTEGER' for field in config['fields']])},
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    conn.commit()
    
    # Coleta dados
    for network, config in social_networks.items():
        print(f"\n🔹 {network}")
        print(f"   (Enter para pular, deixa o valor anterior)")
        
        values = []
        for field in config['fields']:
            field_name = field.replace('_', ' ').title()
            value = input(f"   {field_name}: ").strip()
            
            if value:
                try:
                    values.append(int(value.replace(',', '').replace('.', '')))
                except:
                    print(f"   ⚠️  Valor inválido, pulando...")
                    values.append(0)
            else:
                # Pega último valor
                cursor.execute(f'SELECT {field} FROM {config["table"]} ORDER BY id DESC LIMIT 1')
                last = cursor.fetchone()
                values.append(last[0] if last else 0)
                print(f"   → Mantendo: {values[-1]:,}")
        
        # Insere no banco
        placeholders = ', '.join(['?'] * (len(config['fields']) + 1))
        fields_str = ', '.join(['username'] + config['fields'])
        cursor.execute(
            f'INSERT INTO {config["table"]} ({fields_str}) VALUES ({placeholders})',
            ['crismonteirosp'] + values
        )
        
        print(f"   ✅ {network} salvo!")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Todas as redes sociais atualizadas!")

def main():
    load_dotenv()
    
    print_header("🚀 RADAR DAS REDES - Coleta Completa")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # 1. Instagram (automático)
    collect_instagram()
    
    # 2. Notion (automático)
    collect_notion()
    
    # 3. Redes sociais manuais
    print("\n")
    resposta = input("📱 Atualizar redes sociais manualmente? (s/N): ").strip().lower()
    if resposta == 's':
        collect_manual_social()
    else:
        print("⏭️  Pulando redes sociais manuais...")
    
    print_header("✅ COLETA FINALIZADA")
    print("🎉 Todos os dados foram atualizados!")
    print("💡 Execute o dashboard: python3 scripts/run_complete_dashboard.py")

if __name__ == '__main__':
    main()
