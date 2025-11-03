"""
Modelos de banco de dados para o sistema de monitoramento
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InstagramProfile(Base):
    """Modelo para dados de perfis do Instagram"""
    
    __tablename__ = "instagram_profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, index=True)
    full_name = Column(String(200))
    biography = Column(Text)
    followers = Column(Integer, nullable=False)
    following = Column(Integer, nullable=False)
    posts_count = Column(Integer, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_business = Column(Boolean, default=False)
    profile_pic_url = Column(Text)
    external_url = Column(Text)
    
    # Métricas calculadas
    engagement_rate = Column(Float)  # Taxa de engajamento média
    avg_likes = Column(Float)
    avg_comments = Column(Float)
    
    # Metadados
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_primary = Column(Boolean, default=False)  # Marca perfil principal
    
    # Índices para queries rápidas
    __table_args__ = (
        Index('idx_username_date', 'username', 'collected_at'),
    )
    
    def __repr__(self):
        return f"<InstagramProfile(username='{self.username}', followers={self.followers}, date='{self.collected_at}')>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'biography': self.biography,
            'followers': self.followers,
            'following': self.following,
            'posts_count': self.posts_count,
            'is_verified': self.is_verified,
            'is_business': self.is_business,
            'profile_pic_url': self.profile_pic_url,
            'external_url': self.external_url,
            'engagement_rate': self.engagement_rate,
            'avg_likes': self.avg_likes,
            'avg_comments': self.avg_comments,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None,
            'is_primary': self.is_primary,
        }


class CollectionLog(Base):
    """Log de coletas realizadas"""
    
    __tablename__ = "collection_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(50), nullable=False)  # instagram, youtube, etc
    username = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # success, error, partial
    error_message = Column(Text)
    records_collected = Column(Integer, default=0)
    execution_time = Column(Float)  # em segundos
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<CollectionLog(platform='{self.platform}', username='{self.username}', status='{self.status}')>"


class DailyMetrics(Base):
    """Métricas diárias consolidadas (para análises e gráficos)"""
    
    __tablename__ = "daily_metrics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(50), nullable=False)
    username = Column(String(100), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    # Métricas principais
    followers = Column(Integer, nullable=False)
    following = Column(Integer)
    posts_count = Column(Integer)
    
    # Crescimento
    followers_growth = Column(Integer)  # Diferença do dia anterior
    followers_growth_rate = Column(Float)  # % de crescimento
    
    # Engajamento
    engagement_rate = Column(Float)
    avg_likes = Column(Float)
    avg_comments = Column(Float)
    
    # Índices compostos para queries rápidas
    __table_args__ = (
        Index('idx_username_platform_date', 'username', 'platform', 'date'),
    )
    
    def __repr__(self):
        return f"<DailyMetrics(username='{self.username}', date='{self.date}', followers={self.followers})>"
