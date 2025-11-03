"""
Funções auxiliares e utilitários
"""
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd


def format_number(num: int) -> str:
    """
    Formata número com separador de milhares
    """
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


def calculate_growth_rate(current: int, previous: int) -> float:
    """
    Calcula taxa de crescimento percentual
    """
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def get_date_range(days: int) -> tuple:
    """
    Retorna range de datas (início, fim)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def clean_username(username: str) -> str:
    """
    Remove @ do username se presente
    """
    return username.replace('@', '').strip()


def validate_instagram_username(username: str) -> bool:
    """
    Valida formato de username do Instagram
    """
    username = clean_username(username)
    
    if not username:
        return False
    
    # Instagram: 1-30 caracteres, alfanumérico, underscore e ponto
    if len(username) > 30:
        return False
    
    allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789._')
    return all(c.lower() in allowed_chars for c in username)


def aggregate_metrics(df: pd.DataFrame, by: str = 'username') -> pd.DataFrame:
    """
    Agrega métricas por username
    """
    if df.empty:
        return pd.DataFrame()
    
    agg_dict = {
        'followers': 'last',
        'following': 'last',
        'posts_count': 'last',
        'engagement_rate': 'mean',
        'collected_at': 'max'
    }
    
    return df.groupby(by).agg(agg_dict).reset_index()


def detect_anomalies(values: List[float], threshold: float = 2.0) -> List[bool]:
    """
    Detecta anomalias usando desvio padrão
    """
    if len(values) < 3:
        return [False] * len(values)
    
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = variance ** 0.5
    
    return [abs(v - mean) > threshold * std_dev for v in values]


def estimate_time_to_goal(current: int, goal: int, 
                          avg_daily_growth: float) -> Dict:
    """
    Estima tempo para atingir meta de seguidores
    """
    if avg_daily_growth <= 0:
        return {
            'reachable': False,
            'message': 'Meta não alcançável com crescimento atual'
        }
    
    remaining = goal - current
    
    if remaining <= 0:
        return {
            'reachable': True,
            'days': 0,
            'message': 'Meta já atingida!'
        }
    
    days_needed = remaining / avg_daily_growth
    estimated_date = datetime.now() + timedelta(days=days_needed)
    
    return {
        'reachable': True,
        'days': int(days_needed),
        'estimated_date': estimated_date.strftime('%d/%m/%Y'),
        'message': f'Meta alcançável em aproximadamente {int(days_needed)} dias'
    }


def export_to_csv(df: pd.DataFrame, filename: str):
    """
    Exporta DataFrame para CSV
    """
    df.to_csv(filename, index=False)
    print(f"✅ Dados exportados para: {filename}")


def get_time_of_day_label() -> str:
    """
    Retorna saudação baseada no horário
    """
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"
