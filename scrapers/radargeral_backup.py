#!/usr/bin/env python3
"""
RADAR GERAL - Scraper para monitoramento de todos os políticos brasileiros
Coleta dados do Instagram de 75+ perfis políticos
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from apify_client import ApifyClient
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')
DB_PATH = os.getenv('DATABASE_PATH', 'data/social_monitor.db')

# Lista completa de políticos para monitorar
POLITICOS_RADAR = [
    # TIER 1 - Influência Máxima
    {'username': 'lulaoficial', 'nome': 'Luiz Inácio Lula da Silva', 'cargo': 'Presidente', 'partido': 'PT', 'tier': 1},
    {'username': 'jairmbolsonaro', 'nome': 'Jair Bolsonaro', 'cargo': 'Ex-Presidente', 'partido': 'PL', 'tier': 1},
    {'username': 'geraldoalckmin_', 'nome': 'Geraldo Alckmin', 'cargo': 'Vice-Presidente', 'partido': 'PSB', 'tier': 1},
    {'username': 'hugomottapb', 'nome': 'Hugo Motta', 'cargo': 'Presidente da Câmara', 'partido': 'Republicanos', 'tier': 1},
    {'username': 'davialcolumbre', 'nome': 'Davi Alcolumbre', 'cargo': 'Presidente do Senado', 'partido': 'União Brasil', 'tier': 1},
    {'username': 'tarcisiogdf', 'nome': 'Tarcísio de Freitas', 'cargo': 'Governador SP', 'partido': 'Republicanos', 'tier': 1},
    {'username': 'claudiocastrooficial', 'nome': 'Cláudio Castro', 'cargo': 'Governador RJ', 'partido': 'PL', 'tier': 1},
    {'username': 'romeuzema', 'nome': 'Romeu Zema', 'cargo': 'Governador MG', 'partido': 'Novo', 'tier': 1},
    {'username': 'eduardoleite_', 'nome': 'Eduardo Leite', 'cargo': 'Governador RS', 'partido': 'PSD', 'tier': 1},
    {'username': 'jeronimorodrigues', 'nome': 'Jerônimo Rodrigues', 'cargo': 'Governador BA', 'partido': 'PT', 'tier': 1},
    {'username': 'ronaldocaiado', 'nome': 'Ronaldo Caiado', 'cargo': 'Governador GO', 'partido': 'União Brasil', 'tier': 1},
    {'username': 'ratinhojunior', 'nome': 'Ratinho Junior', 'cargo': 'Governador PR', 'partido': 'PSD', 'tier': 1},
    {'username': 'michellebolsonaro', 'nome': 'Michelle Bolsonaro', 'cargo': 'Ex-Primeira-Dama', 'partido': 'PL', 'tier': 1},
    {'username': 'fernandohaddad', 'nome': 'Fernando Haddad', 'cargo': 'Ministro Fazenda', 'partido': 'PT', 'tier': 1},
    {'username': 'ruicostase', 'nome': 'Rui Costa', 'cargo': 'Ministro Casa Civil', 'partido': 'PT', 'tier': 1},
    
    # TIER 2 - Alta Influência
    {'username': 'nikolas_dm', 'nome': 'Nikolas Ferreira', 'cargo': 'Deputado Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'bolsonaroduardo', 'nome': 'Eduardo Bolsonaro', 'cargo': 'Deputado Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'flaviobolsonaro', 'nome': 'Flávio Bolsonaro', 'cargo': 'Senador', 'partido': 'PL', 'tier': 2},
    {'username': 'carlazambelli38', 'nome': 'Carla Zambelli', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'erikakbhilton', 'nome': 'Erika Hilton', 'cargo': 'Deputada Federal', 'partido': 'PSOL', 'tier': 2},
    {'username': 'andrejanones', 'nome': 'André Janones', 'cargo': 'Deputado Federal', 'partido': 'Avante', 'tier': 2},
    {'username': 'guilhermeboulos', 'nome': 'Guilherme Boulos', 'cargo': 'Deputado Federal', 'partido': 'PSOL', 'tier': 2},
    {'username': 'kim_kataguiri', 'nome': 'Kim Kataguiri', 'cargo': 'Deputado Federal', 'partido': 'União Brasil', 'tier': 2},
    {'username': 'biakicis', 'nome': 'Bia Kicis', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'damaresalves', 'nome': 'Damares Alves', 'cargo': 'Senadora', 'partido': 'Republicanos', 'tier': 2},
    {'username': 'tabataamaralsp', 'nome': 'Tabata Amaral', 'cargo': 'Deputada Federal', 'partido': 'PSB', 'tier': 2},
    {'username': 'fabioteruel', 'nome': 'Fábio Teruel', 'cargo': 'Deputado Federal', 'partido': 'MDB', 'tier': 2},
    {'username': 'senadorcleicinho', 'nome': 'Cleitinho Azevedo', 'cargo': 'Senador', 'partido': 'PL', 'tier': 2},
    {'username': 'carolinedetoni', 'nome': 'Caroline de Toni', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'juliazanatta', 'nome': 'Julia Zanatta', 'cargo': 'Deputada Federal', 'partido': 'PL', 'tier': 2},
    {'username': 'carlosbolsonaro', 'nome': 'Carlos Bolsonaro', 'cargo': 'Vereador RJ', 'partido': 'PL', 'tier': 2},
    {'username': 'zoemartinezok', 'nome': 'Zoe Martinez', 'cargo': 'Vereadora SP', 'partido': 'PL', 'tier': 2},
    {'username': 'helderbarbalho', 'nome': 'Helder Barbalho', 'cargo': 'Governador PA', 'partido': 'MDB', 'tier': 2},
    {'username': 'ibaneis', 'nome': 'Ibaneis Rocha', 'cargo': 'Governador DF', 'partido': 'MDB', 'tier': 2},
    {'username': 'jorginhomello', 'nome': 'Jorginho Mello', 'cargo': 'Governador SC', 'partido': 'PL', 'tier': 2},
    
    # TIER 3 - Influência Regional/Temática
    {'username': 'padilhalex', 'nome': 'Alexandre Padilha', 'cargo': 'Ministro Saúde', 'partido': 'PT', 'tier': 3},
    {'username': 'gleisi', 'nome': 'Gleisi Hoffmann', 'cargo': 'Ministra RI', 'partido': 'PT', 'tier': 3},
    {'username': 'elmanofreitas', 'nome': 'Elmano de Freitas', 'cargo': 'Governador CE', 'partido': 'PT', 'tier': 3},
    {'username': 'fatimabezerran', 'nome': 'Fátima Bezerra', 'cargo': 'Governadora RN', 'partido': 'PT', 'tier': 3},
    {'username': 'raquellyra', 'nome': 'Raquel Lyra', 'cargo': 'Governadora PE', 'partido': 'PSD', 'tier': 3},
    {'username': 'randolfeap', 'nome': 'Randolfe Rodrigues', 'cargo': 'Senador', 'partido': 'Rede', 'tier': 3},
    {'username': 'humbertocostapt', 'nome': 'Humberto Costa', 'cargo': 'Senador', 'partido': 'PT', 'tier': 3},
    {'username': 'marcelofreixo', 'nome': 'Marcelo Freixo', 'cargo': 'Deputado Federal', 'partido': 'PSOL', 'tier': 3},
    {'username': 'pablomarcal1', 'nome': 'Pablo Marçal', 'cargo': 'Empresário/Político', 'partido': 'PRTB', 'tier': 3},
    {'username': 'cirogomes', 'nome': 'Ciro Gomes', 'cargo': 'Ex-Governador', 'partido': 'PDT', 'tier': 3},
    {'username': 'gusttavolima', 'nome': 'Gusttavo Lima', 'cargo': 'Cantor/Empresário', 'partido': 'Solidariedade', 'tier': 3},
]


def init_database():
    """Inicializa tabelas no banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria tabela para o radar geral
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
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_radar_username_date 
        ON radar_geral(username, collected_at DESC)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado!")


def scrape_instagram_batch(usernames, batch_size=10):
    """
    Coleta dados do Instagram em lotes para otimizar créditos da Apify
    """
    client = ApifyClient(APIFY_TOKEN)
    results = []
    
    # Processa em lotes
    for i in range(0, len(usernames), batch_size):
        batch = usernames[i:i + batch_size]
        print(f"\n🔍 Coletando lote {i//batch_size + 1}: {len(batch)} perfis")
        
        # Prepara input para Apify
        run_input = {
            "usernames": batch,
            "resultsLimit": 0,  # Só pega dados do perfil
        }
        
        try:
            # Roda o scraper
            run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
            
            # Coleta resultados
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)
                print(f"  ✓ {item.get('username', 'unknown')}: {item.get('followersCount', 0):,} seguidores")
        
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
        # Calcula engajamento médio
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
        
        # Busca dados adicionais do político
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
            print(f"  ⚠️ Registro duplicado para {profile.get('username')}")
        except Exception as e:
            print(f"  ❌ Erro ao salvar {profile.get('username')}: {e}")
    
    conn.commit()
    conn.close()
    
    return saved_count


def main():
    print("=" * 60)
    print("🎯 RADAR GERAL - Scraper de Políticos Brasileiros")
    print("=" * 60)
    
    # Inicializa banco
    init_database()
    
    # Lista de usernames para coletar
    usernames = [p['username'] for p in POLITICOS_RADAR]
    
    print(f"\n📊 Total de perfis para monitorar: {len(usernames)}")
    print(f"   - Tier 1 (Influência Máxima): {len([p for p in POLITICOS_RADAR if p['tier'] == 1])}")
    print(f"   - Tier 2 (Alta Influência): {len([p for p in POLITICOS_RADAR if p['tier'] == 2])}")
    print(f"   - Tier 3 (Regional/Temático): {len([p for p in POLITICOS_RADAR if p['tier'] == 3])}")
    
    # Coleta dados
    print("\n🚀 Iniciando coleta...")
    profiles = scrape_instagram_batch(usernames, batch_size=15)
    
    # Salva no banco
    print("\n💾 Salvando no banco de dados...")
    saved = save_to_database(profiles)
    
    # Resumo
    print("\n" + "=" * 60)
    print(f"✅ Coleta finalizada!")
    print(f"   - Perfis coletados: {len(profiles)}")
    print(f"   - Registros salvos: {saved}")
    print("=" * 60)


if __name__ == "__main__":
    main()
