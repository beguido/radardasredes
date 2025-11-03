"""
Layout do dashboard principal
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_header():
    """Header do dashboard"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("📊 Social Media Monitor", className="text-center mb-2",
                       style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                html.P("Monitoramento profissional de redes sociais",
                      className="text-center text-muted mb-4")
            ])
        ])
    ], fluid=True, className="bg-light py-4 mb-4")


def create_stats_cards(stats_data):
    """Cards com estatísticas principais"""
    if not stats_data:
        return html.Div()
    
    cards = []
    
    for stat in stats_data:
        card = dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(stat['title'], className="card-title text-muted mb-2"),
                    html.H2(stat['value'], className="card-text mb-0",
                           style={'color': stat.get('color', '#2c3e50'), 'fontWeight': 'bold'}),
                    html.Small(stat.get('subtitle', ''), className="text-muted")
                ])
            ], className="shadow-sm")
        ], width=12, md=6, lg=3, className="mb-3")
        cards.append(card)
    
    return dbc.Row(cards)


def create_filters():
    """Filtros do dashboard"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label("Período de análise:", className="fw-bold"),
                dcc.Dropdown(
                    id='period-dropdown',
                    options=[
                        {'label': 'Últimos 7 dias', 'value': 7},
                        {'label': 'Últimos 15 dias', 'value': 15},
                        {'label': 'Últimos 30 dias', 'value': 30},
                        {'label': 'Últimos 60 dias', 'value': 60},
                        {'label': 'Últimos 90 dias', 'value': 90},
                    ],
                    value=30,
                    clearable=False,
                    className="mb-3"
                )
            ], width=12, md=4),
            
            dbc.Col([
                html.Label("Perfil principal:", className="fw-bold"),
                html.Div(id='primary-profile-display', className="mb-3")
            ], width=12, md=4),
            
            dbc.Col([
                html.Label("Última atualização:", className="fw-bold"),
                html.Div(id='last-update-display', className="mb-3")
            ], width=12, md=4),
        ])
    ], fluid=True)


def create_main_layout():
    """Layout principal do dashboard"""
    return dbc.Container([
        # Header
        create_header(),
        
        # Stats cards (preenchido dinamicamente)
        html.Div(id='stats-cards'),
        
        # Filtros
        create_filters(),
        
        html.Hr(className="my-4"),
        
        # Gráficos principais
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-timeline",
                    type="default",
                    children=dcc.Graph(id='followers-timeline-graph')
                )
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-growth",
                    type="default",
                    children=dcc.Graph(id='growth-rate-graph')
                )
            ], width=12, lg=6, className="mb-4"),
            
            dbc.Col([
                dcc.Loading(
                    id="loading-engagement",
                    type="default",
                    children=dcc.Graph(id='engagement-comparison-graph')
                )
            ], width=12, lg=6, className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-table",
                    type="default",
                    children=dcc.Graph(id='comparison-table-graph')
                )
            ], width=12)
        ], className="mb-4"),
        
        # Botão de atualização
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    "🔄 Coletar Novos Dados",
                    id="refresh-button",
                    color="primary",
                    size="lg",
                    className="w-100"
                ),
                html.Div(id="refresh-status", className="mt-3 text-center")
            ], width=12, md=6, lg=4, className="mx-auto mb-4")
        ]),
        
        # Footer
        html.Hr(className="my-4"),
        html.Footer([
            html.P("Desenvolvido com ❤️ para @crismonteirosp",
                  className="text-center text-muted")
        ], className="py-3"),
        
        # Interval para auto-refresh (opcional)
        dcc.Interval(
            id='interval-component',
            interval=3600*1000,  # 1 hora em millisegundos
            n_intervals=0,
            disabled=True  # Desabilitado por padrão
        )
        
    ], fluid=True, className="py-4")


def get_layout():
    """Retorna o layout completo"""
    return create_main_layout()
