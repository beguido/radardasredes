import sys
sys.path.insert(0, '.')
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from database.db_manager import DatabaseManager
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Radar das Redes</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
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
                min-height: 320px;
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
            }
            
            .followers-count {
                font-size: 36px;
                font-weight: 700;
                color: #ffffff;
                margin: 12px 0 8px 0;
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
df = db.get_instagram_dataframe(days=365)

if len(df) > 0:
    df['collected_at'] = pd.to_datetime(df['collected_at'])
    df = df.sort_values('collected_at')
    
    profiles = df['username'].unique()
    min_dates = {p: df[df['username'] == p]['collected_at'].min() for p in profiles}
    start_date = max(min_dates.values())
    df = df[df['collected_at'] >= start_date]
    
    latest = df.groupby('username').last().reset_index()
    week_ago = datetime.now() - timedelta(days=7)
    month_ago = datetime.now() - timedelta(days=30)
    
    profiles_data = []
    for _, row in latest.iterrows():
        username = row['username']
        current = row['followers']
        
        # Variação 7 dias
        week_data = df[(df['username'] == username) & (df['collected_at'] >= week_ago)]
        week_change_pct = 0
        week_change_abs = 0
        if len(week_data) > 1:
            week_old = week_data['followers'].iloc[0]
            week_change_abs = current - week_old
            week_change_pct = (week_change_abs / week_old * 100)
        
        # Variação 30 dias
        month_data = df[(df['username'] == username) & (df['collected_at'] >= month_ago)]
        month_change_pct = 0
        month_change_abs = 0
        if len(month_data) > 1:
            month_old = month_data['followers'].iloc[0]
            month_change_abs = current - month_old
            month_change_pct = (month_change_abs / month_old * 100)
        
        profiles_data.append({
            'username': username,
            'followers': current,
            'week_change_pct': week_change_pct,
            'week_change_abs': week_change_abs,
            'month_change_pct': month_change_pct,
            'month_change_abs': month_change_abs
        })
    
    names_map = {
        'crismonteirosp': 'Cris Monteiro',
        'adriventurasp': 'Adriana Ventura',
        'leosiqueirabr': 'Leo Siqueira',
        'marinahelenabr': 'Marina Helena'
    }
    
    photos = {
        'crismonteirosp': 'https://ui-avatars.com/api/?name=Cris+Monteiro&size=200&background=10b981&color=fff',
        'marinahelenabr': 'https://ui-avatars.com/api/?name=Marina+Helena&size=200&background=ef4444&color=fff',
        'leosiqueirabr': 'https://ui-avatars.com/api/?name=Leo+Siqueira&size=200&background=3b82f6&color=fff',
        'adriventurasp': 'https://ui-avatars.com/api/?name=Adriana+Ventura&size=200&background=f59e0b&color=fff'
    }
    
    # Ordena: Cris primeiro, depois por seguidores
    cris_profile = [p for p in profiles_data if 'crismont' in p['username']][0]
    other_profiles = sorted([p for p in profiles_data if 'crismont' not in p['username']], 
                           key=lambda x: x['followers'], reverse=True)
    
    all_profiles = [cris_profile] + other_profiles
    
    profile_cards = []
    for p in all_profiles:
        name = names_map.get(p['username'], p['username'])
        photo = photos.get(p['username'], '')
        is_primary = 'crismont' in p['username']
        
        card = html.Div([
            html.Div([
                html.Img(src=photo, className='profile-avatar'),
                html.Div([
                    html.Div(name, style={'fontSize': '18px', 'fontWeight': '600', 'color': '#e2e8f0'}),
                    html.Div(f"@{p['username'].replace('sp', '').replace('br', '')}", 
                            style={'fontSize': '13px', 'color': '#94a3b8'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '16px'}),
            
            html.Div(f"{p['followers']:,.0f}", className='followers-count'),
            html.Div('seguidores', style={'color': '#6b7280', 'fontSize': '12px', 'fontWeight': '500'}),
            
            # Métricas de variação
            html.Div([
                html.Div([
                    html.Div("Variação 7d", className='metric-label'),
                    html.Div(f"+{p['week_change_pct']:.2f}%", className='metric-value'),
                    html.Div(f"+{p['week_change_abs']:,.0f}", className='metric-absolute')
                ], className='metric-item'),
                
                html.Div([
                    html.Div("Variação 30d", className='metric-label'),
                    html.Div(f"+{p['month_change_pct']:.2f}%", className='metric-value'),
                    html.Div(f"+{p['month_change_abs']:,.0f}", className='metric-absolute')
                ], className='metric-item')
            ], className='metric-row')
            
        ], className=f'profile-card {"primary" if is_primary else ""}')
        
        profile_cards.append(dbc.Col(card, width=12, lg=3))
    
    # Gráfico
    fig_main = go.Figure()
    colors = {'marinahelenabr': '#ef4444', 'leosiqueirabr': '#3b82f6', 
              'crismonteirosp': '#10b981', 'adriventurasp': '#f59e0b'}
    
    for username in df['username'].unique():
        data = df[df['username'] == username].sort_values('collected_at')
        name = names_map.get(username, username)
        
        fig_main.add_trace(go.Scatter(
            x=data['collected_at'],
            y=data['followers'],
            name=name,
            mode='lines',
            line=dict(width=2.5, color=colors.get(username, '#6366f1')),
            hovertemplate='<b>%{fullData.name}</b><br><b>%{y:,.0f}</b> seguidores<br>%{x|%d %b %Y}<extra></extra>'
        ))
    
    fig_main.update_layout(
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#d1d5db', family='Inter'),
        xaxis=dict(gridcolor='#1f2937', showgrid=True, title=''),
        yaxis=dict(gridcolor='#1f2937', showgrid=True, title='Seguidores'),
        hovermode='x unified',
        margin=dict(l=60, r=20, t=20, b=60),
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H1("RADAR DAS REDES", className='main-title'),
                html.P("Análise Competitiva de Redes Sociais", className='subtitle')
            ], style={'maxWidth': '1600px', 'margin': '0 auto'})
        ], className='header-container'),
        
        html.Div([
            html.H2("Perfis Monitorados", className='section-title'),
            dbc.Row(profile_cards),
            
            html.Div([
                html.Div("Evolução Histórica Comparativa", 
                        style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '24px', 'color': '#f7fafc'}),
                dcc.Graph(figure=fig_main, config={'displayModeBar': True, 'displaylogo': False})
            ], className='chart-container'),
            
        ], style={'maxWidth': '1600px', 'margin': '0 auto', 'padding': '20px'})
        
    ], style={'minHeight': '100vh', 'paddingBottom': '60px'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("RADAR DAS REDES")
    print("="*60)
    print("📍 http://127.0.0.1:8050")
    print("="*60 + "\n")
    app.run_server(debug=False, host='127.0.0.1', port=8050)
