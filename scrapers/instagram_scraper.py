import os
from apify_client import ApifyClient
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

load_dotenv()

client = ApifyClient(os.getenv('APIFY_API_KEY'))

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
        
        profile_data = {
            'username': first_item.get('ownerUsername', username),
            'followers': first_item.get('followersCount', 0),
            'following': first_item.get('followsCount', 0),
            'posts_count': first_item.get('postsCount', 0),
            'profile_picture': first_item.get('profilePicUrl', ''),
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
        print(f"   ❤️  Total likes: {profile_data['total_likes']:,}")
        print(f"   💬 Total comentários: {profile_data['total_comments']:,}")
        print(f"   📸 Foto: {profile_data['profile_picture'][:50]}...")
        
        return profile_data
        
    except Exception as e:
        print(f"❌ Erro ao coletar @{username}: {e}")
        import traceback
        traceback.print_exc()
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
