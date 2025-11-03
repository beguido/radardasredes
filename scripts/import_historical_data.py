import pandas as pd
import sqlite3
from datetime import datetime

# Lê o CSV
df = pd.read_csv('Radar_das_Redes_-_Dados.csv')

# Converte Data para datetime
df['Data'] = pd.to_datetime(df['Data'], format='%m/%d/%Y')

# Conecta ao banco
conn = sqlite3.connect('data/social_monitor.db')
cursor = conn.cursor()

# Mapeia colunas do CSV para perfis do Instagram
instagram_profiles = {
    'Instagram': 'crismonteirosp',
    'Adriana': 'adriventurasp',
    'Leo': 'leosiqueirabr', 
    'Marina': 'marinahelenabr'
}

total_imported = 0

for col_name, username in instagram_profiles.items():
    if col_name in df.columns:
        for idx, row in df.iterrows():
            # Pula primeiras 15 linhas para Adriana, Leo e Marina
            if col_name in ['Adriana', 'Leo', 'Marina'] and idx < 15:
                continue
                
            date = row['Data']
            followers = row[col_name]
            
            # Verifica se não é NaN
            if pd.notna(followers):
                try:
                    # Remove vírgulas se for string
                    if isinstance(followers, str):
                        followers = followers.replace(',', '')
                    followers_num = int(float(followers))
                    
                    if followers_num > 0:
                        cursor.execute('''
                            INSERT OR REPLACE INTO instagram_profiles 
                            (username, followers, following, posts_count, engagement_rate, collected_at)
                            VALUES (?, ?, 0, 0, 0, ?)
                        ''', (username, followers_num, date.strftime('%Y-%m-%d %H:%M:%S')))
                        total_imported += 1
                        if total_imported % 20 == 0:
                            print(f"✓ {total_imported} registros...")
                except Exception as e:
                    print(f"✗ Linha {idx} - {username}: {e}")

conn.commit()
conn.close()

print(f"\n✅ {total_imported} registros históricos importados!")
print(f"📊 Perfis: {', '.join(instagram_profiles.values())}")
