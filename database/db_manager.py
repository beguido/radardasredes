"""
Gerenciador de banco de dados
"""
from datetime import datetime, timedelta
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import pandas as pd

from config import settings
from database.models import Base, InstagramProfile, CollectionLog, DailyMetrics


class DatabaseManager:
    """Gerenciador centralizado do banco de dados"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DATABASE_PATH
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Cria todas as tabelas no banco"""
        Base.metadata.create_all(self.engine)
        print(f"✅ Tabelas criadas em: {self.db_path}")
    
    @contextmanager
    def get_session(self) -> Session:
        """Context manager para sessões do banco"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ==================== Instagram ====================
    
    def save_instagram_profile(self, profile_data: dict, is_primary: bool = False):
        """Salva dados de perfil do Instagram"""
        with self.get_session() as session:
            profile = InstagramProfile(
                username=profile_data.get('username'),
                full_name=profile_data.get('fullName'),
                biography=profile_data.get('biography'),
                followers=profile_data.get('followersCount', 0),
                following=profile_data.get('followsCount', 0),
                posts_count=profile_data.get('postsCount', 0),
                is_verified=profile_data.get('verified', False),
                is_business=profile_data.get('businessCategoryName') is not None,
                profile_pic_url=profile_data.get('profilePicUrl'),
                external_url=profile_data.get('externalUrl'),
                engagement_rate=profile_data.get('engagement_rate'),
                avg_likes=profile_data.get('avg_likes'),
                avg_comments=profile_data.get('avg_comments'),
                is_primary=is_primary,
                collected_at=datetime.utcnow()
            )
            session.add(profile)
            return profile
    
    def get_instagram_history(self, username: str, days: int = 30):
        """Retorna histórico de um perfil"""
        with self.get_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            profiles = session.query(InstagramProfile).filter(
                InstagramProfile.username == username,
                InstagramProfile.collected_at >= cutoff_date
            ).order_by(InstagramProfile.collected_at).all()
            
            return [p.to_dict() for p in profiles]
    
    def get_latest_instagram_profiles(self):
        """Retorna os dados mais recentes de todos os perfis"""
        with self.get_session() as session:
            # Subquery para pegar a data mais recente de cada username
            subq = session.query(
                InstagramProfile.username,
                func.max(InstagramProfile.collected_at).label('max_date')
            ).group_by(InstagramProfile.username).subquery()
            
            # Join para pegar os perfis completos
            profiles = session.query(InstagramProfile).join(
                subq,
                (InstagramProfile.username == subq.c.username) &
                (InstagramProfile.collected_at == subq.c.max_date)
            ).all()
            
            return [p.to_dict() for p in profiles]
    
    def get_instagram_dataframe(self, username: str = None, days: int = 90):
        """Retorna dados em formato DataFrame para análises"""
        with self.get_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = session.query(InstagramProfile).filter(
                InstagramProfile.collected_at >= cutoff_date
            )
            
            if username:
                query = query.filter(InstagramProfile.username == username)
            
            query = query.order_by(InstagramProfile.username, InstagramProfile.collected_at)
            
            profiles = query.all()
            data = [p.to_dict() for p in profiles]
            
            if not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            df['collected_at'] = pd.to_datetime(df['collected_at'], format='mixed')
            return df
    
    def calculate_growth(self, username: str, days: int = 7):
        """Calcula crescimento de seguidores"""
        with self.get_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            profiles = session.query(InstagramProfile).filter(
                InstagramProfile.username == username,
                InstagramProfile.collected_at >= cutoff_date
            ).order_by(InstagramProfile.collected_at).all()
            
            if len(profiles) < 2:
                return None
            
            first = profiles[0]
            last = profiles[-1]
            
            growth = last.followers - first.followers
            growth_rate = (growth / first.followers * 100) if first.followers > 0 else 0
            
            return {
                'username': username,
                'period_days': days,
                'start_followers': first.followers,
                'end_followers': last.followers,
                'growth': growth,
                'growth_rate': round(growth_rate, 2),
                'start_date': first.collected_at,
                'end_date': last.collected_at
            }
    
    # ==================== Logs ====================
    
    def log_collection(self, platform: str, username: str, status: str,
                      records_collected: int = 0, error_message: str = None,
                      execution_time: float = 0):
        """Registra log de coleta"""
        with self.get_session() as session:
            log = CollectionLog(
                platform=platform,
                username=username,
                status=status,
                error_message=error_message,
                records_collected=records_collected,
                execution_time=execution_time,
                collected_at=datetime.utcnow()
            )
            session.add(log)
            return log
    
    def get_collection_logs(self, limit: int = 100):
        """Retorna logs de coleta"""
        with self.get_session() as session:
            logs = session.query(CollectionLog).order_by(
                desc(CollectionLog.collected_at)
            ).limit(limit).all()
            
            return [{
                'platform': log.platform,
                'username': log.username,
                'status': log.status,
                'error_message': log.error_message,
                'records_collected': log.records_collected,
                'execution_time': log.execution_time,
                'collected_at': log.collected_at.isoformat()
            } for log in logs]
    
    # ==================== Métricas Diárias ====================
    
    def update_daily_metrics(self):
        """Atualiza tabela de métricas diárias consolidadas"""
        with self.get_session() as session:
            # Pega dados únicos por username e dia
            profiles = session.query(InstagramProfile).all()
            
            for profile in profiles:
                date = profile.collected_at.date()
                
                # Verifica se já existe métrica para esse dia
                existing = session.query(DailyMetrics).filter(
                    DailyMetrics.username == profile.username,
                    DailyMetrics.platform == 'instagram',
                    func.date(DailyMetrics.date) == date
                ).first()
                
                if not existing:
                    # Calcula crescimento
                    prev_day = session.query(InstagramProfile).filter(
                        InstagramProfile.username == profile.username,
                        func.date(InstagramProfile.collected_at) == date - timedelta(days=1)
                    ).first()
                    
                    growth = None
                    growth_rate = None
                    
                    if prev_day:
                        growth = profile.followers - prev_day.followers
                        if prev_day.followers > 0:
                            growth_rate = (growth / prev_day.followers) * 100
                    
                    metric = DailyMetrics(
                        platform='instagram',
                        username=profile.username,
                        date=profile.collected_at,
                        followers=profile.followers,
                        following=profile.following,
                        posts_count=profile.posts_count,
                        followers_growth=growth,
                        followers_growth_rate=growth_rate,
                        engagement_rate=profile.engagement_rate,
                        avg_likes=profile.avg_likes,
                        avg_comments=profile.avg_comments
                    )
                    session.add(metric)
            
            session.commit()


# Instância global
db = DatabaseManager()
