from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from database.db_manager import DatabaseManager
import plotly.graph_objs as go
from datetime import datetime, timedelta

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

db = DatabaseManager()
df = db.get_instagram_dataframe(days=30)

# Cards com estatísticas
stats_cards = dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Total Seguidores"),
                html.H2(f"{df['followers'].iloc[-1]:,.0f}" if len(df) > 0 else "0")
            ])
        ])
    ], width=3),
])

# Gráfico simples
if len(df) > 0:
    fig = go.Figure()
    for profile in df['username'].unique():
        profile_data = df[df['username'] == profile]
        fig.add_trace(go.Scatter(
            x=profile_data['collected_at'],
            y=profile_data['followers'],
            name=profile,
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title="Crescimento de Seguidores",
        xaxis_title="Data",
        yaxis_title="Seguidores",
        height=500
    )
else:
    fig = go.Figure()
    fig.add_annotation(text="Nenhum dado disponível", showarrow=False)

app.layout = dbc.Container([
    html.H1("Social Media Monitor", className="mt-4 mb-4"),
    stats_cards,
    html.Hr(),
    dcc.Graph(figure=fig),
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1', port=8050)
