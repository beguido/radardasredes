import sys
sys.path.insert(0, '.')
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from database.db_manager import DatabaseManager
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# CSS customizado estilo TradingView
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Social Media Monitor</title>
        {%favicon%}
        {%css%}
        <style>
            body { 
                background: #131722; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                color: #d1d4dc;
            }
            .metric-card {
                background: #1e222d;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #2a2e39;
                transition: all 0.3s;
            }
            .metric-card:hover {
                border-color: #2962ff;
                transform: translateY(-2px);
            }
            .chart-container {
                background: #1e222d;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #2a2e39;
                margin-bottom: 20px;
            }
            h1, h2, h3, h4, h5, h6 { color: #d1d4dc; }
            .text-muted { color: #787b86 !important; }
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

db = DatabaseManager()
df = db.get_instagram_dataframe(days=30)

if len(df) == 0:
    app.layout = html.Div([
        html.H1("📊 Social Media Monitor", style={'textAlign': 'center', 'marginTop': '50px'}),
        html.P("Nenhum dado disponível", style={'textAlign': 'center', 'color': '#787b86'})
    ])
else:
    df['collected_at'] = pd.to_datetime(df['collected_at'])
    df = df.sort_values('collected_at')
    
    # Calcular crescimento diário
    df['daily_growth'] = df.groupby('username')['followers'].diff()
    
    latest = df.groupby('username').last().reset_index()
    
    # Cards de métricas
    cards = []
    colors = ['#2962ff', '#f23645', '#089981', '#ff6d00']
    for idx, (_, row) in enumerate(latest.iterrows()):
        prev_week = df[(df['username'] == row['username']) & 
                       (df['collected_at'] < datetime.now() - timedelta(days=7))]
        growth = 0
        if len(prev_week) > 0:
            growth = ((row['followers'] - prev_week['followers'].iloc[-1]) / prev_week['followers'].iloc[-1] * 100)
        
        cards.append(
            html.Div([
                html.Div([
                    html.Div(f"@{row['username']}", style={'color': '#787b86', 'fontSize': '12px'}),
                    html.Div(f"{row['followers']:,.0f}", style={'fontSize': '24px', 'fontWeight': 'bold', 'margin': '8px 0'}),
                    html.Div([
                        html.Span("▲ " if growth >= 0 else "▼ ", style={'color': '#089981' if growth >= 0 else '#f23645'}),
                        html.Span(f"{abs(growth):.1f}% semana", style={'color': '#787b86', 'fontSize': '12px'})
                    ])
                ])
            ], className='metric-card', style={'marginBottom': '20px'})
        )
    
    # Gráfico principal - Crescimento com eixo unificado
    fig_main = go.Figure()
    for idx, profile in enumerate(df['username'].unique()):
        data = df[df['username'] == profile]
        fig_main.add_trace(go.Scatter(
            x=data['collected_at'],
            y=data['followers'],
            name=f"@{profile}",
            mode='lines',
            line=dict(width=2, color=colors[idx % len(colors)]),
            fill='tonexty' if idx > 0 else None,
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors[idx % len(colors)][1:])) + [0.1])}"
        ))
    
    fig_main.update_layout(
        plot_bgcolor='#131722',
        paper_bgcolor='#1e222d',
        font=dict(color='#d1d4dc'),
        xaxis=dict(gridcolor='#2a2e39', showgrid=True),
        yaxis=dict(gridcolor='#2a2e39', showgrid=True),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Gráfico crescimento diário
    fig_daily = go.Figure()
    for idx, profile in enumerate(df['username'].unique()):
        data = df[df['username'] == profile].dropna(subset=['daily_growth'])
        fig_daily.add_trace(go.Bar(
            x=data['collected_at'],
            y=data['daily_growth'],
            name=f"@{profile}",
            marker_color=colors[idx % len(colors)]
        ))
    
    fig_daily.update_layout(
        plot_bgcolor='#131722',
        paper_bgcolor='#1e222d',
        font=dict(color='#d1d4dc'),
        xaxis=dict(gridcolor='#2a2e39'),
        yaxis=dict(gridcolor='#2a2e39', title="Novos Seguidores"),
        barmode='group',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    app.layout = html.Div([
        html.Div([
            html.H1("📊 SOCIAL MEDIA MONITOR", style={'marginBottom': '5px', 'fontSize': '28px'}),
            html.P("Monitoramento em Tempo Real", style={'color': '#787b86', 'fontSize': '14px'})
        ], style={'textAlign': 'center', 'padding': '30px 0 20px 0'}),
        
        html.Div([
            html.Div([
                html.Div(cards[:2], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '15px'}),
                html.Div(cards[2:], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '15px'})
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.H5("📈 Crescimento de Seguidores", style={'marginBottom': '15px'}),
                dcc.Graph(figure=fig_main, config={'displayModeBar': False})
            ], className='chart-container'),
            
            html.Div([
                html.H5("📊 Crescimento Diário", style={'marginBottom': '15px'}),
                dcc.Graph(figure=fig_daily, config={'displayModeBar': False})
            ], className='chart-container'),
            
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'})
        
    ], style={'minHeight': '100vh', 'paddingBottom': '50px'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎨 DASHBOARD PREMIUM STYLE TRADINGVIEW")
    print("="*60)
    print("📍 http://127.0.0.1:8050")
    print("="*60 + "\n")
    app.run_server(debug=False, host='127.0.0.1', port=8050)
