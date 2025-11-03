"""
Componentes de gráficos profissionais para o dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

from config import settings


def create_followers_timeline(df: pd.DataFrame):
    """
    Gráfico de linha com evolução de seguidores ao longo do tempo
    """
    if df.empty:
        return go.Figure().add_annotation(
            text="Nenhum dado disponível",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    # Adicionar linha para cada perfil
    for i, username in enumerate(df['username'].unique()):
        df_user = df[df['username'] == username].sort_values('collected_at')
        
        # Destacar perfil principal
        is_primary = username == settings.PRIMARY_PROFILE
        line_width = 4 if is_primary else 2
        
        fig.add_trace(go.Scatter(
            x=df_user['collected_at'],
            y=df_user['followers'],
            mode='lines+markers',
            name=f"@{username}",
            line=dict(
                width=line_width,
                color=settings.DASHBOARD_SETTINGS['color_scheme'][i % len(settings.DASHBOARD_SETTINGS['color_scheme'])]
            ),
            marker=dict(size=6 if is_primary else 4),
            hovertemplate=(
                '<b>@%{fullData.name}</b><br>' +
                'Data: %{x|%d/%m/%Y}<br>' +
                'Seguidores: %{y:,.0f}<br>' +
                '<extra></extra>'
            )
        ))
    
    fig.update_layout(
        title={
            'text': '📈 Evolução de Seguidores',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        xaxis_title='Data',
        yaxis_title='Seguidores',
        hovermode='x unified',
        template=settings.DASHBOARD_SETTINGS['theme'],
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=100, b=50, l=50, r=50)
    )
    
    # Formatar eixo Y com separador de milhares
    fig.update_layout(yaxis=dict(separatethousands=True))
    
    return fig


def create_growth_rate_chart(df: pd.DataFrame, period_days: int = 7):
    """
    Gráfico de barras com taxa de crescimento percentual
    """
    if df.empty:
        return go.Figure().add_annotation(
            text="Nenhum dado disponível",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    growth_data = []
    
    for username in df['username'].unique():
        df_user = df[df['username'] == username].sort_values('collected_at')
        
        if len(df_user) < 2:
            continue
        
        # Pegar período
        cutoff_date = datetime.now() - timedelta(days=period_days)
        df_period = df_user[df_user['collected_at'] >= cutoff_date]
        
        if len(df_period) < 2:
            df_period = df_user.tail(2)
        
        first = df_period.iloc[0]
        last = df_period.iloc[-1]
        
        growth = last['followers'] - first['followers']
        growth_rate = (growth / first['followers'] * 100) if first['followers'] > 0 else 0
        
        growth_data.append({
            'username': username,
            'growth': growth,
            'growth_rate': growth_rate,
            'is_primary': username == settings.PRIMARY_PROFILE
        })
    
    if not growth_data:
        return go.Figure().add_annotation(
            text="Dados insuficientes para calcular crescimento",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    df_growth = pd.DataFrame(growth_data)
    df_growth = df_growth.sort_values('growth_rate', ascending=False)
    
    # Cores: verde para positivo, vermelho para negativo
    colors = ['#27ae60' if x >= 0 else '#e74c3c' for x in df_growth['growth_rate']]
    
    # Destacar perfil principal
    colors = [
        '#f39c12' if row['is_primary'] else color 
        for color, (_, row) in zip(colors, df_growth.iterrows())
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[f"@{u}" for u in df_growth['username']],
            y=df_growth['growth_rate'],
            text=[f"{rate:+.2f}%" for rate in df_growth['growth_rate']],
            textposition='outside',
            marker_color=colors,
            hovertemplate=(
                '<b>%{x}</b><br>' +
                'Crescimento: %{text}<br>' +
                'Novos seguidores: %{customdata:,.0f}<br>' +
                '<extra></extra>'
            ),
            customdata=df_growth['growth'],
        )
    ])
    
    fig.update_layout(
        title={
            'text': f'📊 Taxa de Crescimento ({period_days} dias)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        xaxis_title='Perfil',
        yaxis_title='Crescimento (%)',
        template=settings.DASHBOARD_SETTINGS['theme'],
        height=400,
        margin=dict(t=100, b=50, l=50, r=50),
        showlegend=False
    )
    
    # Adicionar linha zero
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig


def create_comparison_table(df: pd.DataFrame):
    """
    Tabela comparativa com métricas principais
    """
    if df.empty:
        return go.Figure().add_annotation(
            text="Nenhum dado disponível",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Pegar dados mais recentes de cada perfil
    latest_data = []
    
    for username in df['username'].unique():
        df_user = df[df['username'] == username].sort_values('collected_at')
        latest = df_user.iloc[-1]
        
        # Calcular crescimento se tiver dados anteriores
        growth_7d = 0
        if len(df_user) >= 2:
            cutoff_date = datetime.now() - timedelta(days=7)
            df_week = df_user[df_user['collected_at'] >= cutoff_date]
            if len(df_week) >= 2:
                growth_7d = df_week.iloc[-1]['followers'] - df_week.iloc[0]['followers']
        
        latest_data.append({
            'username': f"@{username}",
            'followers': latest['followers'],
            'following': latest['following'],
            'posts': latest['posts_count'],
            'engagement_rate': latest.get('engagement_rate', 0) or 0,
            'growth_7d': growth_7d,
            'is_primary': username == settings.PRIMARY_PROFILE
        })
    
    df_table = pd.DataFrame(latest_data)
    df_table = df_table.sort_values('followers', ascending=False)
    
    # Destacar perfil principal com emoji
    df_table['username'] = df_table.apply(
        lambda row: f"⭐ {row['username']}" if row['is_primary'] else row['username'],
        axis=1
    )
    
    # Formatar números
    df_table['followers_fmt'] = df_table['followers'].apply(lambda x: f"{x:,}")
    df_table['following_fmt'] = df_table['following'].apply(lambda x: f"{x:,}")
    df_table['posts_fmt'] = df_table['posts'].apply(lambda x: f"{x:,}")
    df_table['engagement_fmt'] = df_table['engagement_rate'].apply(lambda x: f"{x:.2f}%")
    df_table['growth_7d_fmt'] = df_table['growth_7d'].apply(lambda x: f"{x:+,}")
    
    # Cores para células
    cell_colors = []
    for _, row in df_table.iterrows():
        if row['is_primary']:
            cell_colors.append(['#fff3cd'] * 6)  # Amarelo claro
        else:
            cell_colors.append(['white'] * 6)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>Perfil</b>', '<b>Seguidores</b>', '<b>Seguindo</b>', 
                   '<b>Posts</b>', '<b>Engajamento</b>', '<b>Crescimento 7d</b>'],
            fill_color='#34495e',
            align='left',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[
                df_table['username'],
                df_table['followers_fmt'],
                df_table['following_fmt'],
                df_table['posts_fmt'],
                df_table['engagement_fmt'],
                df_table['growth_7d_fmt']
            ],
            fill_color=cell_colors,
            align='left',
            font=dict(size=13),
            height=35
        )
    )])
    
    fig.update_layout(
        title={
            'text': '📋 Métricas Atuais',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        height=300,
        margin=dict(t=80, b=20, l=20, r=20)
    )
    
    return fig


def create_engagement_comparison(df: pd.DataFrame):
    """
    Gráfico de barras horizontais comparando engajamento
    """
    if df.empty or 'engagement_rate' not in df.columns:
        return go.Figure().add_annotation(
            text="Dados de engajamento indisponíveis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Pegar dados mais recentes
    latest_data = []
    for username in df['username'].unique():
        df_user = df[df['username'] == username].sort_values('collected_at')
        latest = df_user.iloc[-1]
        
        if latest.get('engagement_rate'):
            latest_data.append({
                'username': username,
                'engagement_rate': latest['engagement_rate'],
                'is_primary': username == settings.PRIMARY_PROFILE
            })
    
    if not latest_data:
        return go.Figure().add_annotation(
            text="Dados de engajamento indisponíveis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    df_eng = pd.DataFrame(latest_data)
    df_eng = df_eng.sort_values('engagement_rate', ascending=True)
    
    colors = ['#f39c12' if row['is_primary'] else '#3498db' 
             for _, row in df_eng.iterrows()]
    
    fig = go.Figure(data=[
        go.Bar(
            y=[f"@{u}" for u in df_eng['username']],
            x=df_eng['engagement_rate'],
            orientation='h',
            text=[f"{rate:.2f}%" for rate in df_eng['engagement_rate']],
            textposition='outside',
            marker_color=colors,
            hovertemplate=(
                '<b>%{y}</b><br>' +
                'Taxa de Engajamento: %{x:.2f}%<br>' +
                '<extra></extra>'
            )
        )
    ])
    
    fig.update_layout(
        title={
            'text': '💬 Comparativo de Engajamento',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        xaxis_title='Taxa de Engajamento (%)',
        yaxis_title='',
        template=settings.DASHBOARD_SETTINGS['theme'],
        height=300,
        margin=dict(t=100, b=50, l=120, r=50),
        showlegend=False
    )
    
    return fig
