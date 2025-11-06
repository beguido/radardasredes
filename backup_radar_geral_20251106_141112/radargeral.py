#!/usr/bin/env python3
"""
RADAR GERAL - Scraper para monitoramento de políticos brasileiros
Versão FINAL com usernames VERIFICADOS via busca no Google
Data: 05/11/2025
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')
DB_PATH = os.getenv('DATABASE_PATH', 'data/social_monitor.db')

# Lista CORRIGIDA - Usernames verificados no Google
POLITICOS_RADAR = [
    # ========================================
    # TIER 1 - INFLUÊNCIA MÁXIMA (17 perfis)
    # ========================================
    {'username': 'lulaoficial', 'nome': 'Luiz Inácio Lula da Silva', 'cargo': 'Presidente', 'partido': 'PT', 'tier': 1},
    {'username': 'jairmessiasbolsonaro', 'nome': 'Jair Bolsonaro', 'cargo': 'Ex-Presidente', 'partido': 'PL', 'tier': 1},  # CORRIGIDO
    {'username': 'geraldoalckmin_', 'nome': 'Geraldo Alckmin', 'cargo': 'Vice-Presidente', 'partido': 'PSB', 'tier': 1},
    {'username': 'hugomottapb', 'nome': 'Hugo Motta', 'cargo': 'Presidente da Câmara', 'partido': 'Republicanos', 'tier': 1},
    {'username': 'davialcolumbre', 'nome': 'Davi Alcolumbre', 'cargo': 'Presidente do Senado', 'partido': 'União Brasil', 'tier': 1},
    {'username': 'tarcisiogdf', 'nome': 'Tarcísio de Freitas', 'cargo': 'Governador SP', 'partido': 'Republicanos', 'tier': 1},
    {'username': 'claudiocastrorj', 'nome': 'Cláudio Castro', 'cargo': 'Governador RJ', 'partido': 'PL', 'tier': 1},  # CORRIGIDO
    {'username': 'romeuzemaoficial', 'nome': 'Romeu Zema', 'cargo': 'Governador MG', 'partido': 'Novo', 'tier': 1},  # CORRIGIDO
    {'username': 'eduardoleite_', 'nome': 'Eduardo Leite', 'cargo': 'Governador RS', 'partido': 'PSDB', 'tier': 1},
    {'username': 'jeronimorodrigues', 'nome': 'Jerônimo Rodrigues', 'cargo': 'Governador BA', 'partido': 'PT', 'tier': 1},
    {'username': 'ronaldocaiado', 'nome': 'Ronaldo Caiado', 'cargo': 'Governador GO', 'partido': 'União Brasil', 'tier': 1},
    {'username': 'ratinhojunior', 'nome': 'Ratinho Junior', 'cargo': 'Governador PR', 'partido': 'PSD', 'tier': 1},
    {'username': 'michellebolsonaro', 'nome': 'Michelle Bolsonaro', 'cargo': 'Ex-Primeira-Dama', 'partido': 'PL', 'tier': 1},
    {'username': 'fernandohaddad', 'nome': 'Fernando Haddad', 'cargo': 'Ministro Fazenda', 'partido': 'PT', 'tier': 1},
    {'username': 'ruicostaoficial', 'nome': 'Rui Costa', 'cargo': 'Ministro Casa Civil', 'partido': 'PT', 'tier': 1},  # CORRIGIDO
    {'username': 'pablomarcal1', 'nome': 'Pablo Marçal', 'cargo': 'Empresário/Político', 'partido': 'PRTB', 'tier': 1},
    {'username': 'gusttavolima', 'nome': 'Gusttavo Lima', 'cargo': 'Cantor/Empresário', 'partido': 'Solidariedade', 'tier': 1},
    
    # ========================================
    # TIER 2 - ALTA INFLUÊNCIA (20 perfis)
    # ========================================
    {'username': 'nikolasferreiradm', 'nome': 'Nikolas Ferreira', 'cargo': 'Deputado Federal', 'partido': 'PL', 'tier': 2},  # CORRIGIDO
    {'username': 'bolsonarosp', 'nome': 'Eduardo Bolsonaro', 'cargo': 'Deputado Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'flaviobolsonaro', 'nome': 'Flávio Bolsonaro', 'cargo': 'Senador', 'partido': 'PL', 'tier': 2},
    {'username': 'carla.zambelli', 'nome': 'Carla Zambelli', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},  # CORRIGIDO
    {'username': 'hilton_erika', 'nome': 'Erika Hilton', 'cargo': 'Deputada Federal', 'partido': 'PSOL', 'tier': 2},  # CORRIGIDO
    {'username': 'andrejanones', 'nome': 'André Janones', 'cargo': 'Deputado Federal', 'partido': 'Avante', 'tier': 2},
    {'username': 'guilhermeboulos.oficial', 'nome': 'Guilherme Boulos', 'cargo': 'Deputado Federal', 'partido': 'PSOL', 'tier': 2},  # CORRIGIDO
    {'username': 'kimkataguiri', 'nome': 'Kim Kataguiri', 'cargo': 'Deputado Federal', 'partido': 'União Brasil', 'tier': 2},
    {'username': 'biakicis', 'nome': 'Bia Kicis', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'damaresalves', 'nome': 'Damares Alves', 'cargo': 'Senadora', 'partido': 'Republicanos', 'tier': 2},
    {'username': 'tabataamaralsp', 'nome': 'Tabata Amaral', 'cargo': 'Deputada Federal', 'partido': 'PSB', 'tier': 2},
    {'username': 'carolinedetoni', 'nome': 'Caroline de Toni', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'juliazanatta', 'nome': 'Julia Zanatta', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'carlosbolsonaro', 'nome': 'Carlos Bolsonaro', 'cargo': 'Vereador RJ', 'partido': 'PL', 'tier': 2},
    {'username': 'helderbarbalho', 'nome': 'Helder Barbalho', 'cargo': 'Governador PA', 'partido': 'MDB', 'tier': 2},
    {'username': 'ibaneis', 'nome': 'Ibaneis Rocha', 'cargo': 'Governador DF', 'partido': 'MDB', 'tier': 2},
    {'username': 'jorginhomello', 'nome': 'Jorginho Mello', 'cargo': 'Governador SC', 'partido': 'PL', 'tier': 2},
    {'username': 'cirogomes', 'nome': 'Ciro Gomes', 'cargo': 'Ex-Governador', 'partido': 'PDT', 'tier': 2},
    {'username': 'marcelofreixo', 'nome': 'Marcelo Freixo', 'cargo': 'Deputado Federal', 'partido': 'PSOL', 'tier': 2},
    {'username': 'elmanofreitas', 'nome': 'Elmano de Freitas', 'cargo': 'Governador CE', 'partido': 'PT', 'tier': 2},
    
    # ========================================
    # TIER 3 - REGIONAL/TEMÁTICO (9 perfis)
    # ========================================
    {'username': 'gleisi', 'nome': 'Gleisi Hoffmann', 'cargo': 'Presidente PT', 'partido': 'PT', 'tier': 3},
    {'username': 'fatimabezerran', 'nome': 'Fátima Bezerra', 'cargo': 'Governadora RN', 'partido': 'PT', 'tier': 3},
    {'username': 'raquellyra', 'nome': 'Raquel Lyra', 'cargo': 'Governadora PE', 'partido': 'PSDB', 'tier': 3},
    {'username': 'randolfeap', 'nome': 'Randolfe Rodrigues', 'cargo': 'Senador', 'partido': 'Rede', 'tier': 3},
    {'username': 'humbertocostapt', 'nome': 'Humberto Costa', 'cargo': 'Senador', 'partido': 'PT', 'tier': 3},
    {'username': 'alexandrepadilha', 'nome': 'Alexandre Padilha', 'cargo': 'Ministro Rel. Inst.', 'partido': 'PT', 'tier': 3},
    {'username': 'marinassilva', 'nome': 'Marina Silva', 'cargo': 'Ministra Meio Ambiente', 'partido': 'Rede', 'tier': 3},
    {'username': 'simonetebetbrasil', 'nome': 'Simone Tebet', 'cargo': 'Ministra Planejamento', 'partido': 'MDB', 'tier': 3},
    {'username': 'camilosantana', 'nome': 'Camilo Santana', 'cargo': 'Ministro da Educação', 'partido': 'PT', 'tier': 3},
]


def init_database():
    """Inicializa tabelas no banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
            UNIQUE(username, DATE(collected_at))
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_radar_username_date 
        ON radar_geral(username, collected_at DESC)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado!")


def scrape_instagram_batch(usernames, batch_size=15):
    """Coleta dados do Instagram em lotes"""
    client = ApifyClient(APIFY_TOKEN)
    results = []
    
    for i in range(0, len(usernames), batch_size):
        batch = usernames[i:i + batch_size]
        print(f"\n🔍 Coletando lote {i//batch_size + 1}: {len(batch)} perfis")
        
        run_input = {
            "usernames": batch,
            "resultsLimit": 12,
        }
        
        try:
            run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
            
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)
                followers = item.get('followersCount', 0)
                print(f"  ✓ {item.get('username', 'unknown')}: {followers:,} seguidores")
        
        except Exception as e:
            print(f"  ❌ Erro no lote: {e}")
            continue
    
    return results


def save_to_database(profiles_data):
    """Salva dados coletados no banco"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    saved_count = 0
    
    for profile in profiles_data:
        posts = profile.get('latestPosts', [])
        if posts:
            total_engagement = sum(
                (post.get('likesCount', 0) + post.get('commentsCount', 0))
                for post in posts
            )
            followers = profile.get('followersCount', 1)
            avg_engagement_rate = (total_engagement / len(posts) / followers * 100) if followers > 0 else 0
            avg_likes = sum(post.get('likesCount', 0) for post in posts) / len(posts)
            avg_comments = sum(post.get('commentsCount', 0) for post in posts) / len(posts)
        else:
            avg_engagement_rate = 0
            avg_likes = 0
            avg_comments = 0
        
        politico_info = next((p for p in POLITICOS_RADAR if p['username'] == profile.get('username')), {})
        
        try:
            cursor.execute('''
                INSERT INTO radar_geral (
                    username, nome, cargo, partido, tier,
                    followers, following, posts_count,
                    avg_engagement_rate, avg_likes, avg_comments,
                    profile_picture_url, collected_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile.get('username'),
                politico_info.get('nome', profile.get('fullName', '')),
                politico_info.get('cargo', ''),
                politico_info.get('partido', ''),
                politico_info.get('tier', 3),
                profile.get('followersCount', 0),
                profile.get('followingCount', 0),
                profile.get('postsCount', 0),
                avg_engagement_rate,
                avg_likes,
                avg_comments,
                profile.get('profilePicUrl', ''),
                datetime.now()
            ))
            saved_count += 1
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print(f"  ❌ Erro ao salvar {profile.get('username')}: {e}")
    
    conn.commit()
    conn.close()
    
    return saved_count


def main():
    print("=" * 60)
    print("🎯 RADAR GERAL - Versão CORRIGIDA")
    print("=" * 60)
    
    init_database()
    
    usernames = [p['username'] for p in POLITICOS_RADAR]
    
    print(f"\n📊 Total de perfis: {len(usernames)}")
    print(f"   - Tier 1: {len([p for p in POLITICOS_RADAR if p['tier'] == 1])}")
    print(f"   - Tier 2: {len([p for p in POLITICOS_RADAR if p['tier'] == 2])}")
    print(f"   - Tier 3: {len([p for p in POLITICOS_RADAR if p['tier'] == 3])}")
    
    print("\n🚀 Iniciando coleta...")
    profiles = scrape_instagram_batch(usernames, batch_size=15)
    
    print("\n💾 Salvando no banco...")
    saved = save_to_database(profiles)
    
    print("\n" + "=" * 60)
    print(f"✅ Coleta finalizada!")
    print(f"   - Perfis coletados: {len(profiles)}")
    print(f"   - Registros salvos: {saved}")
    print("=" * 60)


if __name__ == "__main__":
    main()
