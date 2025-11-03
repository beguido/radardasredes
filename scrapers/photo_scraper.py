import requests
from bs4 import BeautifulSoup
import json

def get_instagram_photo(username):
    """Pega a foto de perfil do Instagram"""
    try:
        # URL pública do Instagram
        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Tenta pegar via API pública (pode não funcionar sempre)
        response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, timeout=5)
        
        # Procura pela URL da foto no HTML
        if 'profile_pic_url' in response.text:
            start = response.text.find('"profile_pic_url":"') + len('"profile_pic_url":"')
            end = response.text.find('"', start)
            photo_url = response.text[start:end].replace('\\u0026', '&')
            return photo_url
        
        # Fallback: usar avatar do UI Avatars
        return f"https://ui-avatars.com/api/?name={username}&size=200&background=random"
    except:
        return f"https://ui-avatars.com/api/?name={username}&size=200&background=random"

# Cache de fotos
photos = {
    'crismonteirosp': get_instagram_photo('crismonteirosp'),
    'marinahelenabr': get_instagram_photo('marinahelenabr'),
    'leosiqueirabr': get_instagram_photo('leosiqueirabr'),
    'adriventurasp': get_instagram_photo('adriventurasp')
}

print(json.dumps(photos, indent=2))
