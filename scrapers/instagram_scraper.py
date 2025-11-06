import os
from apify_client import ApifyClient
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
import requests

# Carrega variáveis de ambiente do .env
load_dotenv()

# Pega o token
APIFY_TOKEN = os.getenv('APIFY_API_KEY') or os.getenv('APIFY_TOKEN')

if not APIFY_TOKEN:
    print("❌ ERRO: Token do Apify não encontrado!")
    exit(1)

client = ApifyClient(APIFY_TOKEN)

def download_profile_pic(username, url):
    """Baixa e salva foto de perfil localmente"""
    try:
        pics_dir = 'assets/profile_pics'
        os.makedirs(pics_dir, exist_ok=True)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        filename = f"{username}.jpg"
        filepath = os.path.join(pics_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return f"/assets/profile_pics/{filename}"
    except:
        return url  # Se falhar, retorna a URL original

def scrape_instagram_profile(username):
    """Scrape completo de perfil do Instagram via Apify"""
    
    run_input = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": 12,
        "searchType": "user",
        "searchLimit": 1,
        "addParentData": True,
    }
    
    print(f"🔍 Coletando dados de @{username}...")
    
    try:
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)
        
        if not results:
            print(f"❌ Nenhum dado encontrado para @{username}")
            return None
        
        first_item = results[0]
        
        # Baixa a foto de perfil
        original_url = first_item.get('profilePicUrl', '')
        local_pic_path = download_profile_pic(username, original_url) if original_url else ''
        
        profile_data = {
            'username': first_item.get('ownerUsername', username),
            'followers': first_item.get('followersCount', 0),
            'following': first_item.get('followsCount', 0),
            'posts_count': first_item.get('postsCount', 0),
            'profile_picture': local_pic_path,
        }
        
        posts_data = []
        for item in results:
            if item.get('likesCount') is not None:
                posts_data.append({
                    'likes': item.get('likesCount', 0),
                    'comments': item.get('commentsCount', 0),
                })
        
        if profile_data['followers'] == 0:
            print(f"❌ Dados do perfil incompletos")
            return None
        
        if posts_data and profile_data['followers'] > 0:
            total_likes = sum(p['likes'] for p in posts_data)
            total_comments = sum(p['comments'] for p in posts_data)
            total_interactions = total_likes + total_comments
            
            avg_engagement = (total_interactions / len(posts_data)) / profile_data['followers'] * 100
            
            profile_data['avg_engagement_rate'] = avg_engagement
            profile_data['total_likes'] = total_likes
            profile_data['total_comments'] = total_comments
            profile_data['posts_analyzed'] = len(posts_data)
        else:
            profile_data['avg_engagement_rate'] = 0
            profile_data['total_likes'] = 0
            profile_data['total_comments'] = 0
            profile_data['posts_analyzed'] = 0
        
        print(f"✅ @{username}: {profile_data['followers']:,} seguidores")
        print(f"   📊 Engajamento: {profile_data['avg_engagement_rate']:.2f}%")
        print(f"   📸 Foto salva localmente!")
        
        return profile_data
        
    except Exception as e:
        print(f"❌ Erro ao coletar @{username}: {e}")
        return None

def save_to_database(profile_data):
    """Salva os dados no banco"""
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO instagram_profiles 
        (username, followers, following, posts_count, engagement_rate, 
         profile_picture_url, avg_engagement_rate, total_likes, total_comments, posts_analyzed, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        profile_data['username'],
        profile_data['followers'],
        profile_data['following'],
        profile_data['posts_count'],
        profile_data['avg_engagement_rate'],
        profile_data['profile_picture'],
        profile_data['avg_engagement_rate'],
        profile_data['total_likes'],
        profile_data['total_comments'],
        profile_data['posts_analyzed'],
        now
    ))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    profiles = ['crismonteirosp', 'marinahelenabr', 'leosiqueirabr', 'adriventurasp']
    
    print("\n" + "="*60)
    print("📸 INSTAGRAM SCRAPER - Coleta Completa")
    print("="*60 + "\n")
    
    for username in profiles:
        data = scrape_instagram_profile(username)
        if data:
            save_to_database(data)
            print(f"💾 Dados salvos no banco!\n")
        else:
            print(f"⚠️  Falha ao coletar dados\n")
    
    print("="*60)
    print("✅ Coleta finalizada!")
    print("="*60)
