"""
Scraper de Instagram usando Apify
"""
import time
from typing import List, Dict
from apify_client import ApifyClient

from config import settings
from database import db


class InstagramScraper:
    """Scraper profissional de Instagram via Apify"""
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or settings.APIFY_API_TOKEN
        self.client = ApifyClient(self.api_token)
        self.scraper_id = settings.APIFY_INSTAGRAM_SCRAPER
    
    def scrape_profile(self, username: str) -> Dict:
        """
        Scrape de um perfil do Instagram
        
        Args:
            username: Nome de usuário sem @
            
        Returns:
            Dicionário com dados do perfil
        """
        # Remove @ se presente
        username = username.replace('@', '')
        
        print(f"🔍 Coletando dados de @{username}...")
        
        # Configuração do scraper
        run_input = {
            "usernames": [username],
            "resultsLimit": 1,
            "resultsType": "profiles",
            "searchLimit": 1,
            "searchType": "user",
            "addParentData": False,
        }
        
        try:
            # Executar o scraper
            run = self.client.actor(self.scraper_id).call(run_input=run_input)
            
            # Aguardar e pegar resultados
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)
            
            if not results:
                raise ValueError(f"Nenhum dado encontrado para @{username}")
            
            profile_data = results[0]
            
            # Enriquecer com métricas calculadas (se tiver posts)
            if 'latestPosts' in profile_data and profile_data['latestPosts']:
                posts = profile_data['latestPosts'][:12]  # Últimos 12 posts
                
                total_likes = sum(post.get('likesCount', 0) for post in posts)
                total_comments = sum(post.get('commentsCount', 0) for post in posts)
                
                avg_likes = total_likes / len(posts) if posts else 0
                avg_comments = total_comments / len(posts) if posts else 0
                
                # Taxa de engajamento = (likes + comments) / followers
                followers = profile_data.get('followersCount', 1)
                if followers > 0:
                    engagement_rate = ((avg_likes + avg_comments) / followers) * 100
                else:
                    engagement_rate = 0
                
                profile_data['avg_likes'] = round(avg_likes, 2)
                profile_data['avg_comments'] = round(avg_comments, 2)
                profile_data['engagement_rate'] = round(engagement_rate, 2)
            
            print(f"✅ Dados coletados: @{username} - {profile_data.get('followersCount', 0):,} seguidores")
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Erro ao coletar @{username}: {str(e)}")
            raise e
    
    def scrape_multiple_profiles(self, usernames: List[str], 
                                 primary_username: str = None) -> List[Dict]:
        """
        Scrape de múltiplos perfis
        
        Args:
            usernames: Lista de usernames
            primary_username: Username principal (para marcar no banco)
            
        Returns:
            Lista de dicionários com dados dos perfis
        """
        results = []
        
        for i, username in enumerate(usernames, 1):
            try:
                start_time = time.time()
                
                # Coletar dados
                profile_data = self.scrape_profile(username)
                
                # Determinar se é perfil principal
                is_primary = (username.replace('@', '') == primary_username)
                
                # Salvar no banco
                db.save_instagram_profile(profile_data, is_primary=is_primary)
                
                execution_time = time.time() - start_time
                
                # Log de sucesso
                db.log_collection(
                    platform='instagram',
                    username=username,
                    status='success',
                    records_collected=1,
                    execution_time=execution_time
                )
                
                results.append(profile_data)
                
                # Aguardar entre requisições (rate limiting gentil)
                if i < len(usernames):
                    wait_time = settings.COLLECTION_SETTINGS['wait_between_profiles']
                    print(f"⏳ Aguardando {wait_time}s antes do próximo perfil...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                # Log de erro
                db.log_collection(
                    platform='instagram',
                    username=username,
                    status='error',
                    error_message=str(e)
                )
                print(f"❌ Erro ao processar @{username}: {str(e)}")
                continue
        
        return results
    
    def get_account_info(self) -> Dict:
        """Verifica informações da conta Apify"""
        try:
            user = self.client.user().get()
            return {
                'username': user.get('username'),
                'email': user.get('email'),
                'plan': user.get('plan'),
                'credits': 'Ver painel',
            }
        except Exception as e:
            return {'error': str(e)}


def run_instagram_collection():
    """
    Função auxiliar para executar coleta completa do Instagram
    """
    print("=" * 60)
    print("🚀 INICIANDO COLETA DE DADOS - INSTAGRAM")
    print("=" * 60)
    
    scraper = InstagramScraper()
    
    # Verificar conta Apify
    account_info = scraper.get_account_info()
    if 'error' not in account_info:
        print(f"\n💳 Conta Apify: {account_info.get('username')}")
        print(f"📊 Plano: {account_info.get('plan')}")
        print("💰 Créditos: Ver painel")
    
    # Coletar dados
    profiles = settings.INSTAGRAM_PROFILES
    primary = settings.PRIMARY_PROFILE
    
    print(f"📋 Perfis para coletar: {len(profiles)}")
    print(f"⭐ Perfil principal: @{primary}\n")
    
    results = scraper.scrape_multiple_profiles(profiles, primary_username=primary)
    
    print("\n" + "=" * 60)
    print(f"✅ COLETA FINALIZADA: {len(results)}/{len(profiles)} perfis coletados")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    run_instagram_collection()
