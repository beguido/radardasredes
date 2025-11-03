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
        <title>Radar das Redes - Analytics</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            body { 
                background: #0a0e1a;
                font-family: 'Inter', sans-serif;
                color: #e2e8f0;
                margin: 0;
                padding: 0;
            }
            
            .header-container {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 40px 20px;
                border-bottom: 2px solid #334155;
            }
            
            .main-title {
                font-size: 36px;
                font-weight: 800;
                margin: 0;
                color: #ffffff;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            
            .subtitle {
                font-size: 14px;
                color: #94a3b8;
                margin-top: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border-radius: 16px;
                padding: 24px;
                margin: 10px;
                border: 1px solid #334155;
                transition: all 0.3s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
                border-color: #3b82f6;
            }
            
            .metric-label {
                font-size: 12px;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
                font-weight: 600;
            }
            
            .metric-value {
                font-size: 32px;
                font-weight: 800;
                color: #ffffff;
                margin: 8px 0;
            }
            
            .metric-subtitle {
                font-size: 13px;
                color: #94a3b8;
            }
            
            .projection-card {
                background: #1e293b;
                border-radius: 12px;
                padding: 20px;
                margin: 8px 0;
                border-left: 4px solid #3b82f6;
            }
            
            .projection-date {
                font-size: 14px;
                color: #3b82f6;
                font-weight: 700;
                text-transform: uppercase;
                margin-bottom: 8px;
            }
            
            .projection-value {
                font-size: 28px;
                font-weight: 800;
                color: #ffffff;
            }
            
            .section-title {
                font-size: 24px;
                font-weight: 700;
                color: #ffffff;
                margin: 60px 0 30px 0;
                padding-bottom: 16px;
                border-bottom: 2px solid #334155;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .chart-container {
                background: #1e293b;
                border-radius: 16px;
                padding: 32px;
                margin: 20px 0;
                border: 1px solid #334155;
            }
            
            .score-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 700;
                margin: 8px 4px;
            }
            
            .score-excellent {
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
            }
            
            .score-good {
                background: linear-gradient(135deg, #3b82f6, #2563eb);
                color: white;
            }
            
            .score-warning {
                background: linear-gradient(135deg, #f59e0b, #d97706);
                color: white;
            }
            
            .score-critical {
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
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

# Carrega dados
conn = sqlite3.connect('data/social_monitor.db')
df = pd.read_sql_query("SELECT * FROM instagram_profiles ORDER BY collected_at", conn)
conn.close()

if len(df) > 0:
    df['collected_at'] = pd.to_datetime(df['collected_at'], format='mixed')
    
    # Instancia o motor de analytics
    analytics = AnalyticsEngine(df)
    
    # Pega dados mais recentes com engajamento
    df_with_engagement = df[df['avg_engagement_rate'] > 0]
    if len(df_with_engagement) > 0:
        latest = df_with_engagement.groupby('username').last().reset_index()
    else:
        latest = df.groupby('username').last().reset_index()
    
    names_map = {
        'crismonteirosp': 'Cris Monteiro',
        'adriventurasp': 'Adriana Ventura',
        'leosiqueirabr': 'Leo Siqueira',
        'marinahelenabr': 'Marina Helena'
    }
    
    colors = {
        'marinahelenabr': '#ef4444',
        'leosiqueirabr': '#3b82f6', 
        'crismonteirosp': '#10b981',
        'adriventurasp': '#f59e0b'
    }
    
    # === PROJEÇÕES PARA DATAS IMPORTANTES ===
    projections_section = []
    
    for username in latest['username']:
        name = names_map.get(username, username)
        color = colors.get(username, '#6366f1')
        
        proj_ano_novo = analytics.project_followers(username, DATA_ANO_NOVO_2026)
        proj_campanha = analytics.project_followers(username, DATA_INICIO_CAMPANHA_2026)
        proj_eleicao_1t = analytics.project_followers(username, DATA_ELEICAO_1T_2026)
        proj_eleicao_2t = analytics.project_followers(username, DATA_ELEICAO_2T_2026)
        
        current = latest[latest['username'] == username].iloc[0]['followers']
        
        proj_card = html.Div([
            html.H3(name, style={'color': color, 'fontSize': '20px', 'fontWeight': '700', 'marginBottom': '20px'}),
            html.Div([
                html.Div([
                    html.Div("ATUAL", className='projection-date', style={'borderColor': color}),
                    html.Div(f"{current:,.0f}", className='projection-value'),
                    html.Div("seguidores", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'})
                ], className='projection-card', style={'borderColor': color}),
                
                html.Div([
                    html.Div("1º DE JANEIRO 2026", className='projection-date'),
                    html.Div(f"{proj_ano_novo:,.0f}", className='projection-value'),
                    html.Div(f"+{proj_ano_novo - current:,.0f} ({((proj_ano_novo - current) / current * 100):.1f}%)", 
                            style={'fontSize': '12px', 'color': '#10b981', 'marginTop': '4px'})
                ], className='projection-card'),
                
                html.Div([
                    html.Div("INÍCIO CAMPANHA (16/08/2026)", className='projection-date'),
                    html.Div(f"{proj_campanha:,.0f}", className='projection-value'),
                    html.Div(f"+{proj_campanha - current:,.0f} ({((proj_campanha - current) / current * 100):.1f}%)", 
                            style={'fontSize': '12px', 'color': '#10b981', 'marginTop': '4px'})
                ], className='projection-card'),
                
                html.Div([
                    html.Div("ELEIÇÃO 1º TURNO (04/10/2026)", className='projection-date'),
                    html.Div(f"{proj_eleicao_1t:,.0f}", className='projection-value'),
                    html.Div(f"+{proj_eleicao_1t - current:,.0f} ({((proj_eleicao_1t - current) / current * 100):.1f}%)", 
                            style={'fontSize': '12px', 'color': '#10b981', 'marginTop': '4px'})
                ], className='projection-card'),
                
                html.Div([
                    html.Div("ELEIÇÃO 2º TURNO (25/10/2026)", className='projection-date'),
                    html.Div(f"{proj_eleicao_2t:,.0f}", className='projection-value'),
                    html.Div(f"+{proj_eleicao_2t - current:,.0f} ({((proj_eleicao_2t - current) / current * 100):.1f}%)", 
                            style={'fontSize': '12px', 'color': '#10b981', 'marginTop': '4px'})
                ], className='projection-card'),
            ])
        ], style={'marginBottom': '40px'})
        
        projections_section.append(dbc.Col(proj_card, width=12, lg=6, xl=3))
    
    # === MÉTRICAS AVANÇADAS ===
    metrics_cards = []
    
    for username in latest['username']:
        name = names_map.get(username, username)
        color = colors.get(username, '#6366f1')
        
        score = analytics.calculate_performance_score(username)
        momentum = analytics.calculate_momentum(username)
        daily_growth = analytics.calculate_daily_average_growth(username)
        health = analytics.get_health_status(username)
        
        card = html.Div([
            html.H4(name, style={'color': color, 'marginBottom': '20px', 'fontSize': '18px', 'fontWeight': '700'}),
            
            html.Div([
                html.Div("PERFORMANCE SCORE", className='metric-label'),
                html.Div(f"{score:.0f}/100", className='metric-value', style={'color': color}),
                html.Div(health, style={'fontSize': '14px', 'marginTop': '8px'})
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Div("CRESCIMENTO DIÁRIO", className='metric-label'),
                html.Div(f"+{daily_growth:.0f}", className='metric-value', style={'fontSize': '24px'}),
                html.Div("seguidores/dia", className='metric-subtitle')
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Div("MOMENTUM", className='metric-label'),
                html.Div(f"{momentum:+.2f}%", className='metric-value', 
                        style={'fontSize': '24px', 'color': '#10b981' if momentum > 0 else '#ef4444'}),
                html.Div("aceleração" if momentum > 0 else "desaceleração", className='metric-subtitle')
            ])
            
        ], className='metric-card')
        
        metrics_cards.append(dbc.Col(card, width=12, lg=6, xl=3))
    
    # Layout
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H1("🎯 RADAR DAS REDES", className='main-title'),
                html.P("Analytics & Projeções Eleitorais 2026", className='subtitle')
            ], style={'maxWidth': '1800px', 'margin': '0 auto'})
        ], className='header-container'),
        
        html.Div([
            html.H2("📊 PERFORMANCE SCORE & MÉTRICAS", className='section-title'),
            dbc.Row(metrics_cards),
            
            html.H2("🔮 PROJEÇÕES PARA DATAS IMPORTANTES", className='section-title'),
            dbc.Row(projections_section),
            
        ], style={'maxWidth': '1800px', 'margin': '0 auto', 'padding': '40px 20px'})
        
    ], style={'minHeight': '100vh', 'paddingBottom': '80px'})

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎯 RADAR DAS REDES - ANALYTICS AVANÇADO")
    print("="*70)
    print("📍 http://127.0.0.1:8050")
    print("="*70 + "\n")
    app.run_server(debug=False, host='127.0.0.1', port=8050)
