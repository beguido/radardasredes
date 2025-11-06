import os
import sqlite3
import requests
from datetime import datetime

def download_profile_pictures():
    """Baixa fotos de perfil e salva localmente"""
    
    # Cria pasta se não existir
    pics_dir = 'assets/profile_pics'
    os.makedirs(pics_dir, exist_ok=True)
    
    # Conecta no banco
    conn = sqlite3.connect('data/social_monitor.db')
    cursor = conn.cursor()
    
    # Pega as fotos mais recentes de cada perfil
    cursor.execute('''
        SELECT DISTINCT username, profile_picture_url 
        FROM instagram_profiles 
        WHERE profile_picture_url IS NOT NULL 
        AND profile_picture_url != ''
        GROUP BY username
        HAVING collected_at = MAX(collected_at)
    ''')
    
    profiles = cursor.fetchall()
    
    print("\n" + "="*60)
    print("📸 DOWNLOAD DE FOTOS DE PERFIL")
    print("="*60 + "\n")
    
    for username, url in profiles:
        if not url:
            continue
            
        try:
            print(f"📥 Baixando foto de @{username}...")
            
            # Baixa a imagem
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Salva localmente
            filename = f"{username}.jpg"
            filepath = os.path.join(pics_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Atualiza o banco com o caminho local
            local_path = f"/assets/profile_pics/{filename}"
            cursor.execute('''
                UPDATE instagram_profiles 
                SET profile_picture_url = ? 
                WHERE username = ?
            ''', (local_path, username))
            
            print(f"✅ Salvo em: {filepath}")
            
        except Exception as e:
            print(f"❌ Erro ao baixar @{username}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ Download concluído!")
    print("="*60 + "\n")

if __name__ == '__main__':
    download_profile_pictures()
