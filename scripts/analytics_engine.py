import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

class AnalyticsEngine:
    """Motor de análise avançada para métricas de performance"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['collected_at'] = pd.to_datetime(self.df['collected_at'])
        self.df = self.df.sort_values('collected_at')
    
    def calculate_growth_rate(self, username, days=7):
        """Calcula taxa de crescimento"""
        user_data = self.df[self.df['username'] == username].tail(days)
        if len(user_data) < 2:
            return 0
        
        first = user_data.iloc[0]['followers']
        last = user_data.iloc[-1]['followers']
        
        if first == 0:
            return 0
        
        return ((last - first) / first) * 100
    
    def calculate_daily_average_growth(self, username, days=30):
        """Média de seguidores ganhos por dia"""
        user_data = self.df[self.df['username'] == username].tail(days)
        if len(user_data) < 2:
            return 0
        
        total_growth = user_data.iloc[-1]['followers'] - user_data.iloc[0]['followers']
        days_diff = (user_data.iloc[-1]['collected_at'] - user_data.iloc[0]['collected_at']).days
        
        if days_diff == 0:
            return 0
        
        return total_growth / days_diff
    
    def project_followers(self, username, target_date):
        """Projeta seguidores para uma data futura"""
        user_data = self.df[self.df['username'] == username].tail(30)
        
        if len(user_data) < 2:
            return user_data.iloc[-1]['followers'] if len(user_data) > 0 else 0
        
        # Regressão linear
        user_data['days'] = (user_data['collected_at'] - user_data['collected_at'].min()).dt.days
        
        if user_data['days'].std() == 0:
            return user_data.iloc[-1]['followers']
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            user_data['days'], 
            user_data['followers']
        )
        
        # Calcula dias até a data alvo
        current_date = user_data['collected_at'].max()
        days_until_target = (target_date - current_date).days
        
        if days_until_target < 0:
            return user_data.iloc[-1]['followers']
        
        # Projeção
        current_days = user_data['days'].max()
        projected = slope * (current_days + days_until_target) + intercept
        
        # Não permite valores negativos
        return max(0, int(projected))
    
    def calculate_momentum(self, username):
        """Calcula momentum (aceleração do crescimento)"""
        user_data = self.df[self.df['username'] == username].tail(14)
        
        if len(user_data) < 4:
            return 0
        
        # Divide em duas metades
        mid = len(user_data) // 2
        first_half = user_data.iloc[:mid]
        second_half = user_data.iloc[mid:]
        
        growth_first = self.calculate_growth_rate_from_data(first_half)
        growth_second = self.calculate_growth_rate_from_data(second_half)
        
        return growth_second - growth_first
    
    def calculate_growth_rate_from_data(self, data):
        """Helper para calcular taxa de crescimento de um subset"""
        if len(data) < 2:
            return 0
        first = data.iloc[0]['followers']
        last = data.iloc[-1]['followers']
        if first == 0:
            return 0
        return ((last - first) / first) * 100
    
    def calculate_performance_score(self, username):
        """Calcula score de performance (0-100)"""
        latest = self.df[self.df['username'] == username].iloc[-1]
        
        # Componentes do score
        engagement = min(latest.get('avg_engagement_rate', 0) * 10, 40)  # Max 40 pontos
        growth_7d = min(self.calculate_growth_rate(username, 7) * 5, 30)  # Max 30 pontos
        growth_30d = min(self.calculate_growth_rate(username, 30) * 2, 20)  # Max 20 pontos
        momentum_score = min(abs(self.calculate_momentum(username)), 10)  # Max 10 pontos
        
        total = engagement + growth_7d + growth_30d + momentum_score
        
        return min(100, max(0, total))
    
    def calculate_engagement_quality(self, username):
        """Score de qualidade do engajamento"""
        latest = self.df[self.df['username'] == username].iloc[-1]
        
        total_likes = latest.get('total_likes', 0)
        total_comments = latest.get('total_comments', 0)
        
        # Comentários valem 3x mais que likes
        quality = (total_comments * 3 + total_likes) / latest['followers'] * 100
        
        return quality
    
    def get_health_status(self, username):
        """Status de saúde do perfil"""
        score = self.calculate_performance_score(username)
        momentum = self.calculate_momentum(username)
        
        if score >= 70 and momentum > 0:
            return "🔥 Excelente"
        elif score >= 50 and momentum >= 0:
            return "✅ Saudável"
        elif score >= 30:
            return "⚠️ Atenção"
        else:
            return "❌ Crítico"
