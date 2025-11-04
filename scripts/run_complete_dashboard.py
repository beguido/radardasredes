import sys
sys.path.insert(0, '.')
from scripts.analytics_engine import AnalyticsEngine
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import os

# Datas importantes
DATA_ANO_NOVO_2026 = datetime(2026, 1, 1)
DATA_INICIO_CAMPANHA_2026 = datetime(2026, 8, 16)
DATA_ELEICAO_1T_2026 = datetime(2026, 10, 4)
DATA_ELEICAO_2T_2026 = datetime(2026, 10, 25)

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'))

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Radar das Redes</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            body { 
                background: #0f1419;
                font-family: 'Inter', sans-serif;
                color: #d1d5db;
                margin: 0;
                padding: 0;
            }
            
            .header-container {
                background: #1a1f2e;
                padding: 32px 20px;
                border-bottom: 1px solid #2d3748;
            }
            
            .main-title {
                font-size: 32px;
                font-weight: 600;
                margin: 0;
                color: #f7fafc;
            }
            
            .subtitle {
                font-size: 14px;
                color: #9ca3af;
                margin-top: 4px;
            }
            
            .profile-card {
                background: #1a1f2e;
                border-radius: 12px;
                padding: 24px;
                margin: 10px;
                border: 1px solid #2d3748;
                transition: all 0.2s ease;
                min-height: 420px;
            }
            
            .profile-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 32px rgba(0,0,0,0.4);
                border-color: #3b82f6;
            }
            
            .profile-card.primary {
                border: 2px solid #10b981;
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            }
            
            .profile-avatar {
                width: 64px;
                height: 64px;
                border-radius: 50%;
                margin-right: 16px;
                border: 3px solid #334155;
                object-fit: cover;
            }
            
            .followers-count {
                font-size: 36px;
                font-weight: 700;
                color: #ffffff;
                margin: 12px 0 8px 0;
            }
            
            .engagement-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                margin: 8px 0;
            }
            
            .engagement-high {
                background: rgba(16, 185, 129, 0.15);
                color: #10b981;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            
            .engagement-medium {
                background: rgba(251, 191, 36, 0.15);
                color: #fbbf24;
                border: 1px solid rgba(251, 191, 36, 0.3);
            }
            
            .engagement-low {
                background: rgba(239, 68, 68, 0.15);
                color: #ef4444;
                border: 1px solid rgba(239, 68, 68, 0.3);
            }
            
            .metric-row {
                display: flex;
                justify-content: space-between;
                margin-top: 16px;
                padding-top: 16px;
                border-top: 1px solid #2d3748;
            }
            
            .metric-item {
                flex: 1;
            }
            
            .metric-label {
                font-size: 11px;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 4px;
            }
            
            .metric-value {
                font-size: 15px;
                font-weight: 600;
                color: #10b981;
            }
            
            .metric-absolute {
                font-size: 12px;
                color: #6b7280;
                margin-top: 2px;
            }
            
            .chart-container {
                background: #1a1f2e;
                border-radius: 12px;
                padding: 32px;
                margin: 30px 0;
                border: 1px solid #2d3748;
            }
            
            .section-title {
                font-size: 20px;
                font-weight: 600;
                color: #f7fafc;
                margin: 48px 0 24px 0;
                padding-bottom: 12px;
                border-bottom: 1px solid #2d3748;
            }
            
            .projection-mini {
                background: #0f1419;
                border-radius: 8px;
                padding: 12px;
                margin-top: 12px;
            }
            
            .projection-mini-label {
                font-size: 10px;
                color: #64748b;
                text-transform: uppercase;
                margin-bottom: 4px;
            }
            
            .projection-mini-value {
                font-size: 16px;
                font-weight: 700;
                color: #3b82f6;
            }
            
            .score-badge {
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                margin-left: 8px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

conn = sqlite3.connect('data/social_monitor.db')
df = pd.read_sql_query("SELECT * FROM instagram_profiles ORDER BY collected_at", conn)
conn.close()

if len(df) > 0:
    df['collected_at'] = pd.to_datetime(df['collected_at'], format='mixed')
    df = df.sort_values('collected_at')
    
    # Analytics engine
    analytics = AnalyticsEngine(df)
    # Dados do Notion
    conn_notion = sqlite3.connect('data/social_monitor.db')
    notion_latest = pd.read_sql_query("""
        SELECT whatsapp, enderecos, oficios, collected_at
        FROM notion_stats
        ORDER BY id DESC
        LIMIT 2
    """, conn_notion)
    conn_notion.close()
    
    notion_current = notion_latest.iloc[0] if len(notion_latest) > 0 else None
    notion_previous = notion_latest.iloc[1] if len(notion_latest) > 1 else None
    
    whatsapp_total = notion_current['whatsapp'] if notion_current is not None else 0
    enderecos_total = notion_current['enderecos'] if notion_current is not None else 0
    oficios_total = notion_current['oficios'] if notion_current is not None else 0
    
    whatsapp_change = whatsapp_total - (notion_previous['whatsapp'] if notion_previous is not None else whatsapp_total)
    enderecos_change = enderecos_total - (notion_previous['enderecos'] if notion_previous is not None else enderecos_total)
    oficios_change = oficios_total - (notion_previous['oficios'] if notion_previous is not None else oficios_total)

    
    profiles = df['username'].unique()
    min_dates = {p: df[df['username'] == p]['collected_at'].min() for p in profiles}
    start_date = max(min_dates.values())
    df_filtered = df[df['collected_at'] >= start_date]
    
    df_with_engagement = df[df['avg_engagement_rate'] > 0]
    if len(df_with_engagement) > 0:
        latest = df_with_engagement.groupby('username').last().reset_index()
    else:
        latest = df.groupby('username').last().reset_index()
    
    day_ago = datetime.now() - timedelta(days=1)
    week_ago = datetime.now() - timedelta(days=7)
    month_ago = datetime.now() - timedelta(days=30)
    quarter_ago = datetime.now() - timedelta(days=90)
    
    profiles_data = []
    for _, row in latest.iterrows():
        username = row['username']
        current = row['followers']
        
        # 1 dia
        day_data = df[(df['username'] == username) & (df['collected_at'] >= day_ago)]
        day_change_pct = 0
        day_change_abs = 0
        if len(day_data) > 1:
            day_old = day_data['followers'].iloc[0]
            day_change_abs = current - day_old
            day_change_pct = (day_change_abs / day_old * 100) if day_old > 0 else 0
        
        # 7 dias
        week_data = df[(df['username'] == username) & (df['collected_at'] >= week_ago)]
        week_change_pct = 0
        week_change_abs = 0
        if len(week_data) > 1:
            week_old = week_data['followers'].iloc[0]
            week_change_abs = current - week_old
            week_change_pct = (week_change_abs / week_old * 100)
        
        # 30 dias
        month_data = df[(df['username'] == username) & (df['collected_at'] >= month_ago)]
        month_change_pct = 0
        month_change_abs = 0
        if len(month_data) > 1:
            month_old = month_data['followers'].iloc[0]
            month_change_abs = current - month_old
            month_change_pct = (month_change_abs / month_old * 100)
        
        # 90 dias
        quarter_data = df[(df['username'] == username) & (df['collected_at'] >= quarter_ago)]
        quarter_change_pct = 0
        quarter_change_abs = 0
        if len(quarter_data) > 1:
            quarter_old = quarter_data['followers'].iloc[0]
            quarter_change_abs = current - quarter_old
            quarter_change_pct = (quarter_change_abs / quarter_old * 100)
        
        photo_path = row.get('profile_picture_url', '')
        if photo_path and photo_path.startswith('/static'):
            photo_url = app.get_asset_url(photo_path.replace('/static/', ''))
        else:
            photo_url = ''
        
        # Projeções
        proj_eleicao = analytics.project_followers(username, DATA_ELEICAO_1T_2026)
        proj_ano_novo = analytics.project_followers(username, DATA_ANO_NOVO_2026)
        proj_campanha = analytics.project_followers(username, DATA_INICIO_CAMPANHA_2026)
        score = analytics.calculate_performance_score(username)
        
        profiles_data.append({
            'username': username,
            'followers': current,
            'day_change_pct': day_change_pct,
            'day_change_abs': day_change_abs,
            'week_change_pct': week_change_pct,
            'week_change_abs': week_change_abs,
            'month_change_pct': month_change_pct,
            'month_change_abs': month_change_abs,
            'quarter_change_pct': quarter_change_pct,
            'quarter_change_abs': quarter_change_abs,
            'engagement': row.get('avg_engagement_rate', 0),
            'photo': photo_url,
            'proj_eleicao': proj_eleicao,
            'proj_ano_novo': proj_ano_novo,
            'proj_campanha': proj_campanha,
            'score': score
        })
    
    names_map = {
        'crismonteirosp': 'Cris Monteiro',
        'adriventurasp': 'Adriana Ventura',
        'leosiqueirabr': 'Leo Siqueira',
        'marinahelenabr': 'Marina Helena'
    }
    
    colors = {'marinahelenabr': '#ef4444', 'leosiqueirabr': '#3b82f6', 
              'crismonteirosp': '#10b981', 'adriventurasp': '#f59e0b'}
    
    cris_profile = [p for p in profiles_data if 'crismont' in p['username']][0]
    other_profiles = sorted([p for p in profiles_data if 'crismont' not in p['username']], 
                           key=lambda x: x['followers'], reverse=True)
    
    all_profiles = [cris_profile] + other_profiles
    
    profile_cards = []
    for p in all_profiles:
        name = names_map.get(p['username'], p['username'])
        is_primary = 'crismont' in p['username']
        
        eng = p['engagement']
        if eng >= 5:
            eng_class = 'engagement-high'
            eng_emoji = '🔥'
        elif eng >= 3:
            eng_class = 'engagement-medium'
            eng_emoji = '📊'
        else:
            eng_class = 'engagement-low'
            eng_emoji = '📉'
        
        score_color = '#10b981' if p['score'] >= 50 else '#f59e0b' if p['score'] >= 30 else '#ef4444'
        
        card = html.Div([
            html.Div([
                html.Img(src=p['photo'], className='profile-avatar') if p['photo'] else html.Div('👤', style={'width': '64px', 'height': '64px', 'borderRadius': '50%', 'background': 'linear-gradient(135deg, #3b82f6, #8b5cf6)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'fontSize': '24px', 'marginRight': '16px'}),
                html.Div([
                    html.Div([
                        html.Span(name, style={'fontSize': '18px', 'fontWeight': '600', 'color': '#e2e8f0'}),
                        html.Span(f"{p['score']:.0f}", className='score-badge', style={'background': score_color, 'color': 'white'})
                    ]),
                    html.Div(f"@{p['username'].replace('sp', '').replace('br', '')}", 
                            style={'fontSize': '13px', 'color': '#94a3b8'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '16px'}),
            
            html.Div(f"{p['followers']:,.0f}", className='followers-count'),
            html.Div('seguidores', style={'color': '#6b7280', 'fontSize': '12px', 'fontWeight': '500'}),
            
            html.Div(
                f"{eng_emoji} {eng:.2f}% engajamento",
                className=f'engagement-badge {eng_class}'
            ),
            
            html.Div([
                html.Div([
                    html.Div("Variação 1d", className='metric-label'),
                    html.Div(f"+{p['day_change_pct']:.2f}%", className='metric-value', style={'fontSize': '14px'}),
                    html.Div(f"+{p['day_change_abs']:,.0f}", className='metric-absolute')
                ], className='metric-item'),
                
                html.Div([
                    html.Div("Variação 7d", className='metric-label'),
                    html.Div(f"+{p['week_change_pct']:.2f}%", className='metric-value', style={'fontSize': '14px'}),
                    html.Div(f"+{p['week_change_abs']:,.0f}", className='metric-absolute')
                ], className='metric-item')
            ], className='metric-row'),
            
            html.Div([
                html.Div([
                    html.Div("Variação 30d", className='metric-label'),
                    html.Div(f"+{p['month_change_pct']:.2f}%", className='metric-value', style={'fontSize': '14px'}),
                    html.Div(f"+{p['month_change_abs']:,.0f}", className='metric-absolute')
                ], className='metric-item'),
                
                html.Div([
                    html.Div("Variação 90d", className='metric-label'),
                    html.Div(f"+{p['quarter_change_pct']:.2f}%", className='metric-value', style={'fontSize': '14px'}),
                    html.Div(f"+{p['quarter_change_abs']:,.0f}", className='metric-absolute')
                ], className='metric-item')
            ], className='metric-row'),
            
            html.Div([
                html.Div("🗳️ ELEIÇÃO 1º TURNO (04/10/2026)", className='projection-mini-label'),
                html.Div(f"{p['proj_eleicao']:,.0f}", className='projection-mini-value', style={'fontSize': '18px'}),
                html.Div("seguidores projetados", style={'fontSize': '10px', 'color': '#64748b', 'marginTop': '2px'})
            ], className='projection-mini'),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div("📅 1º Jan 2026", style={'fontSize': '9px', 'color': '#64748b', 'marginBottom': '2px'}),
                        html.Div(f"{p['proj_ano_novo']:,.0f}", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#6366f1'})
                    ], style={'flex': 1}),
                    html.Div([
                        html.Div("📢 Campanha", style={'fontSize': '9px', 'color': '#64748b', 'marginBottom': '2px'}),
                        html.Div(f"{p['proj_campanha']:,.0f}", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#8b5cf6'})
                    ], style={'flex': 1})
                ], style={'display': 'flex', 'gap': '8px'})
            ], style={'marginTop': '8px', 'padding': '8px', 'background': '#0a0e1a', 'borderRadius': '6px'})
            
        ], className=f'profile-card {"primary" if is_primary else ""}')
        
        profile_cards.append(dbc.Col(card, width=12, lg=3))
    
    # Gráfico de Seguidores
    fig_followers = go.Figure()
    
    for username in df_filtered['username'].unique():
        data = df_filtered[df_filtered['username'] == username].sort_values('collected_at')
        name = names_map.get(username, username)
        
        fig_followers.add_trace(go.Scatter(
            x=data['collected_at'],
            y=data['followers'],
            name=name,
            mode='lines',
            line=dict(width=2.5, color=colors.get(username, '#6366f1')),
            hovertemplate='<b>%{fullData.name}</b><br><b>%{y:,.0f}</b> seguidores<br>%{x|%d %b %Y}<extra></extra>'
        ))
    
    fig_followers.update_layout(
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#d1d5db', family='Inter'),
        xaxis=dict(gridcolor='#1f2937', showgrid=True, title=''),
        yaxis=dict(gridcolor='#1f2937', showgrid=True, title='Seguidores'),
        hovermode='x unified',
        margin=dict(l=60, r=20, t=20, b=60),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    
    # Gráfico de Engajamento
    fig_engagement = go.Figure()
    
    engagement_data = []
    for username in profiles:
        user_data = latest[latest['username'] == username]
        if len(user_data) > 0 and user_data.iloc[0].get('avg_engagement_rate', 0) > 0:
            engagement_data.append({
                'name': names_map.get(username, username),
                'engagement': user_data.iloc[0].get('avg_engagement_rate', 0),
                'color': colors.get(username, '#6366f1')
            })
    
    engagement_data = sorted(engagement_data, key=lambda x: x['engagement'], reverse=True)
    
    fig_engagement.add_trace(go.Bar(
        x=[d['name'] for d in engagement_data],
        y=[d['engagement'] for d in engagement_data],
        marker=dict(color=[d['color'] for d in engagement_data]),
        text=[f"{d['engagement']:.2f}%" for d in engagement_data],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Engajamento: %{y:.2f}%<extra></extra>'
    ))
    
    fig_engagement.update_layout(
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#d1d5db', family='Inter'),
        xaxis=dict(gridcolor='#1f2937', showgrid=False, title=''),
        yaxis=dict(gridcolor='#1f2937', showgrid=True, title='Taxa de Engajamento (%)'),
        margin=dict(l=60, r=20, t=20, b=60),
        height=400,
        showlegend=False
    )
    
    # === GRÁFICO DE PERFORMANCE SCORE ===
    fig_score = go.Figure()
    
    for username in df_filtered['username'].unique():
        data = df_filtered[df_filtered['username'] == username].sort_values('collected_at')
        name = names_map.get(username, username)
        
        # Calcula score para cada ponto
        scores = []
        for idx, row in data.iterrows():
            temp_df = df[df['username'] == username]
            temp_df = temp_df[temp_df['collected_at'] <= row['collected_at']]
            if len(temp_df) >= 2:
                temp_analytics = AnalyticsEngine(temp_df)
                score = temp_analytics.calculate_performance_score(username)
                scores.append(score)
            else:
                scores.append(0)
        
        fig_score.add_trace(go.Scatter(
            x=data['collected_at'],
            y=scores,
            name=name,
            mode='lines+markers',
            line=dict(width=2.5, color=colors.get(username, '#6366f1')),
            marker=dict(size=6),
            hovertemplate='<b>%{fullData.name}</b><br>Score: %{y:.0f}/100<br>%{x|%d %b %Y}<extra></extra>'
        ))
    
    fig_score.update_layout(
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#d1d5db', family='Inter'),
        xaxis=dict(gridcolor='#1f2937', showgrid=True, title=''),
        yaxis=dict(gridcolor='#1f2937', showgrid=True, title='Performance Score', range=[0, 100]),
        hovermode='x unified',
        margin=dict(l=60, r=20, t=20, b=60),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    
    # === GRÁFICO DE EXPLOSÕES DE CRESCIMENTO ===
    fig_velocity = go.Figure()
    
    for username in df_filtered['username'].unique():
        data = df_filtered[df_filtered['username'] == username].sort_values('collected_at')
        name = names_map.get(username, username)
        
        # Calcula crescimento diário
        velocities = []
        dates = []
        for i in range(1, len(data)):
            days_diff = (data.iloc[i]['collected_at'] - data.iloc[i-1]['collected_at']).days
            if days_diff > 0:
                growth = data.iloc[i]['followers'] - data.iloc[i-1]['followers']
                velocity = growth / days_diff
                velocities.append(velocity)
                dates.append(data.iloc[i]['collected_at'])
        
        fig_velocity.add_trace(go.Bar(
            x=dates,
            y=velocities,
            name=name,
            marker=dict(color=colors.get(username, '#6366f1')),
            hovertemplate='<b>%{fullData.name}</b><br>+%{y:.0f} seguidores/dia<br>%{x|%d %b %Y}<extra></extra>'
        ))
    
    fig_velocity.update_layout(
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#d1d5db', family='Inter'),
        xaxis=dict(gridcolor='#1f2937', showgrid=True, title=''),
        yaxis=dict(gridcolor='#1f2937', showgrid=True, title='Seguidores Ganhos por Dia'),
        hovermode='x unified',
        margin=dict(l=60, r=20, t=20, b=60),
        height=450,
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    
    # === SCATTER: ENGAJAMENTO vs MOMENTUM ===
    fig_scatter = go.Figure()
    
    for username in latest['username']:
        name = names_map.get(username, username)
        row = latest[latest['username'] == username].iloc[0]
        
        engagement = row.get('avg_engagement_rate', 0)
        momentum = analytics.calculate_momentum(username)
        followers = row['followers']
        
        fig_scatter.add_trace(go.Scatter(
            x=[engagement],
            y=[momentum],
            name=name,
            mode='markers+text',
            marker=dict(
                size=followers/5000,  # Tamanho proporcional aos seguidores
                color=colors.get(username, '#6366f1'),
                line=dict(width=2, color='white')
            ),
            text=[name],
            textposition='top center',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{fullData.name}</b><br>Engajamento: %{x:.2f}%<br>Momentum: %{y:+.2f}%<br><extra></extra>'
        ))
    
    fig_scatter.update_layout(
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#d1d5db', family='Inter'),
        xaxis=dict(gridcolor='#1f2937', showgrid=True, title='Taxa de Engajamento (%)'),
        yaxis=dict(gridcolor='#1f2937', showgrid=True, title='Momentum (Aceleração %)', zeroline=True, zerolinecolor='#374151'),
        margin=dict(l=60, r=20, t=20, b=60),
        height=450,
        showlegend=False,
        annotations=[
            dict(x=0.02, y=0.98, xref='paper', yref='paper', text='🔥 Alto Engajamento<br>Acelerando', showarrow=False, xanchor='left', yanchor='top', font=dict(size=10, color='#10b981')),
            dict(x=0.02, y=0.02, xref='paper', yref='paper', text='🔥 Alto Engajamento<br>Desacelerando', showarrow=False, xanchor='left', yanchor='bottom', font=dict(size=10, color='#f59e0b')),
            dict(x=0.98, y=0.98, xref='paper', yref='paper', text='⚠️ Baixo Engajamento<br>Acelerando', showarrow=False, xanchor='right', yanchor='top', font=dict(size=10, color='#3b82f6')),
            dict(x=0.98, y=0.02, xref='paper', yref='paper', text='❌ Baixo Engajamento<br>Desacelerando', showarrow=False, xanchor='right', yanchor='bottom', font=dict(size=10, color='#ef4444'))
        ]
    )
    
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H1("RADAR DAS REDES", className='main-title'),
                html.P("Análise Competitiva & Projeções Eleitorais 2026", className='subtitle')
            ], style={'maxWidth': '1600px', 'margin': '0 auto'})
        ], className='header-container'),
        
        html.Div([
            html.H2("Perfis Monitorados", className='section-title'),
            dbc.Row(profile_cards),
            
            html.Div([
                html.Div("Evolução de Seguidores", 
                        style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '24px', 'color': '#f7fafc'}),
                dcc.Graph(figure=fig_followers, config={'displayModeBar': True, 'displaylogo': False})
            ], className='chart-container'),
            
            html.Div([
                html.Div("Ranking de Engajamento", 
                        style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '24px', 'color': '#f7fafc'}),
                dcc.Graph(figure=fig_engagement, config={'displayModeBar': True, 'displaylogo': False})
            ], className='chart-container'),
            
            html.Div([
                html.Div("Performance Score ao Longo do Tempo", 
                        style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '24px', 'color': '#f7fafc'}),
                dcc.Graph(figure=fig_score, config={'displayModeBar': True, 'displaylogo': False})
            ], className='chart-container'),
            
            html.Div([
                html.Div("Velocidade de Crescimento (Detecta Explosões)", 
                        style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '24px', 'color': '#f7fafc'}),
                dcc.Graph(figure=fig_velocity, config={'displayModeBar': True, 'displaylogo': False})
            ], className='chart-container'),
            
            html.Div([
                html.Div("Análise: Engajamento vs Momentum", 
                        style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '24px', 'color': '#f7fafc'}),
                html.P("Tamanho das bolhas = número de seguidores. Quadrante superior esquerdo = melhor posição.", 
                      style={'fontSize': '12px', 'color': '#9ca3af', 'marginBottom': '16px'}),
                dcc.Graph(figure=fig_scatter, config={'displayModeBar': True, 'displaylogo': False})
            ], className='chart-container'),
            
        ], style={'maxWidth': '1600px', 'margin': '0 auto', 'padding': '20px'})
        
    ], style={'minHeight': '100vh', 'paddingBottom': '60px'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("RADAR DAS REDES - Dashboard Completo")
    print("="*60)
    print("📍 http://127.0.0.1:8050")
    print("="*60 + "\n")
    app.run_server(debug=False, host='127.0.0.1', port=8050)
