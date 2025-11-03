import sys
sys.path.insert(0, '.')
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from database.db_manager import DatabaseManager
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd

# Tema moderno
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

db = DatabaseManager()

def create_app_layout():
    df = db.get_instagram_dataframe(days=30)
    
    if len(df) == 0:
        return dbc.Container([
            html.Div([
                html.H1("📊 Social Media Monitor", className="text-center mt-5"),
                dbc.Alert("Nenhum dado disponível. Execute a coleta primeiro!", color="warning")
            ])
        ])
    
    # Cards de métricas
    latest = df.groupby('username').last().reset_index()
    
    cards = []
    for _, row in latest.iterrows():
        cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(f"@{row['username']}", className="text-muted"),
                        html.H3(f"{row['followers']:,.0f}", className="mb-0"),
                        html.Small("seguidores", className="text-muted")
                    ])
                ], className="shadow-sm")
            ], width=3)
        )
    
    # Gráfico de crescimento
    fig_growth = go.Figure()
    for profile in df['username'].unique():
        data = df[df['username'] == profile].sort_values('collected_at')
        fig_growth.add_trace(go.Scatter(
            x=data['collected_at'],
            y=data['followers'],
            name=f"@{profile}",
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig_growth.update_layout(
        title="📈 Crescimento de Seguidores",
        xaxis_title="Data",
        yaxis_title="Seguidores",
        height=400,
        hovermode='x unified',
        template='plotly_white',
        font=dict(family="Arial, sans-serif")
    )
    
    # Gráfico de comparação
    fig_compare = go.Figure(data=[
        go.Bar(
            x=[f"@{row['username']}" for _, row in latest.iterrows()],
            y=latest['followers'],
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=latest['followers'].apply(lambda x: f"{x:,.0f}"),
            textposition='auto',
        )
    ])
    
    fig_compare.update_layout(
        title="📊 Comparação de Perfis",
        xaxis_title="Perfil",
        yaxis_title="Seguidores",
        height=400,
        template='plotly_white',
        font=dict(family="Arial, sans-serif")
    )
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("📊 Social Media Monitor", className="text-center mt-4 mb-0"),
                html.P("Monitoramento de Redes Sociais", className="text-center text-muted mb-4")
            ])
        ]),
        
        html.Hr(),
        
        # Cards de métricas
        dbc.Row(cards, className="mb-4"),
        
        # Gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=fig_growth, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm mb-4")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=fig_compare, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm")
            ], width=12)
        ]),
        
        # Footer
        html.Hr(className="mt-5"),
        html.P(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
               className="text-center text-muted mb-4 small")
        
    ], fluid=True, className="px-4")

app.layout = create_app_layout()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DASHBOARD MODERNO RODANDO")
    print("="*60)
    print(f"📍 URL: http://127.0.0.1:8050")
    print(f"💡 Pressione Ctrl+C para parar")
    print("="*60 + "\n")
    app.run_server(debug=False, host='127.0.0.1', port=8050)
