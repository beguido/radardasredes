import sqlite3
import requests
import os
from pathlib import Path

def download_profile_photos():
    """Baixa as fotos de perfil e salva localmente"""
    
    # Cria diretório se não existir
    photos_dir = Path('static/profile_photos')
    photos_dir.mkdir(parents=True, exist_ok=True)
    
    # Conecta ao banco
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    
    # Pega as URLs das fotos mais recentes (que são URLs do Instagram, não locais)
    cursor.execute('''
        SELECT username, profile_picture_url 
        FROM instagram_profiles 
        WHERE profile_picture_url IS NOT NULL 
        AND profile_picture_url != ''
        AND profile_picture_url LIKE 'http%'
        AND avg_engagement_rate > 0
        ORDER BY collected_at DESC
    ''')
    
    # Remove duplicatas mantendo a mais recente
    seen = set()
    profiles = []
    for username, photo_url in cursor.fetchall():
        if username not in seen:
            profiles.append((username, photo_url))
            seen.add(username)
    
    print("\n" + "="*60)
    print("📸 DOWNLOAD DE FOTOS DE PERFIL")
    print("="*60 + "\n")
    
    for username, photo_url in profiles:
        if not photo_url or not photo_url.startswith('http'):
            continue
            
        try:
            print(f"📥 Baixando foto de @{username}...")
            print(f"   URL: {photo_url[:60]}...")
            
            # Baixa a imagem
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(photo_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Salva localmente
            filename = f"{username}.jpg"
            filepath = photos_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Salva: {filepath} ({len(response.content)} bytes)")
            
        except Exception as e:
            print(f"❌ Erro ao baixar @{username}: {e}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ Download concluído!")
    print("="*60)

if __name__ == '__main__':
    download_profile_photos()
