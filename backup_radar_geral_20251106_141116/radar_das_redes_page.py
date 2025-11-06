#!/usr/bin/env python3
"""
RADAR DAS REDES - Página do Dashboard
Monitoramento de 75+ políticos brasileiros no Instagram
"""

import sys
sys.path.insert(0, '.')
from dash import Dash, html, dcc, Input, Output, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configuração
DB_PATH = os.getenv('DATABASE_PATH', 'data/social_monitor.db')

# Cores por tier
TIER_COLORS = {
    1: '#FFD700',  # Dourado - Influência Máxima
    2: '#90EE90',  # Verde Claro - Alta Influência
    3: '#87CEEB'   # Azul Claro - Regional/Temático
}

TIER_LABELS = {
    1: 'Influência Máxima',
    2: 'Alta Influência',
    3: 'Regional/Temático'
}


def get_politicos_data():
    """Busca dados mais recentes de todos os políticos"""
    conn = sqlite3.connect(DB_PATH)
    
    query = '''
        SELECT 
            r1.username,
            r1.nome,
            r1.cargo,
            r1.partido,
            r1.tier,
            r1.followers,
            r1.avg_engagement_rate,
            r1.avg_likes,
            r1.avg_comments,
            r1.profile_picture_url,
            r1.collected_at,
            -- Crescimento 7 dias
            CASE 
                WHEN r7.followers IS NOT NULL AND r7.followers > 0
                THEN ((r1.followers - r7.followers) * 100.0 / r7.followers)
                ELSE 0
            END as growth_7d,
            -- Crescimento 30 dias
            CASE 
                WHEN r30.followers IS NOT NULL AND r30.followers > 0
                THEN ((r1.followers - r30.followers) * 100.0 / r30.followers)
                ELSE 0
            END as growth_30d
        FROM radar_geral r1
        LEFT JOIN radar_geral r7 ON r1.username = r7.username 
            AND DATE(r7.collected_at) = DATE(r1.collected_at, '-7 days')
        LEFT JOIN radar_geral r30 ON r1.username = r30.username 
            AND DATE(r30.collected_at) = DATE(r1.collected_at, '-30 days')
        WHERE r1.collected_at = (
            SELECT MAX(collected_at) 
            FROM radar_geral r2 
            WHERE r2.username = r1.username
        )
        ORDER BY r1.tier ASC, r1.followers DESC
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df


def create_politico_card(politico):
    """Cria card de um político"""
    
    # Usa avatar genérico (Instagram bloqueia CORS)
    foto_url = f"https://ui-avatars.com/api/?name={politico['nome']}&size=200&background=random&bold=true"
    
    # Cor baseada no tier
    tier_color = TIER_COLORS.get(politico['tier'], '#87CEEB')
    
    # Ícone de variação
    growth_7d = politico.get('growth_7d', 0)
    if growth_7d > 0:
        arrow_icon = "↗"
        arrow_color = "#10b981"
    elif growth_7d < 0:
        arrow_icon = "↘"
        arrow_color = "#ef4444"
    else:
        arrow_icon = "→"
        arrow_color = "#6b7280"
    
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                # Header com foto e tier badge
                html.Div([
                    html.Img(
                        src=foto_url,
                        style={
                            'width': '80px',
                            'height': '80px',
                            'borderRadius': '50%',
                            'objectFit': 'cover',
                            'border': f'3px solid {tier_color}'
                        }
                    ),
                    html.Div([
                        html.H5(
                            politico['nome'],
                            style={
                                'margin': '0',
                                'fontSize': '16px',
                                'fontWeight': 'bold',
                                'color': '#fff'
                            }
                        ),
                        html.P(
                            f"{politico['cargo']} • {politico['partido']}",
                            style={
                                'margin': '4px 0 0 0',
                                'fontSize': '12px',
                                'color': '#9ca3af'
                            }
                        ),
                        html.Span(
                            TIER_LABELS[politico['tier']],
                            style={
                                'fontSize': '10px',
                                'padding': '2px 8px',
                                'borderRadius': '12px',
                                'backgroundColor': tier_color + '20',
                                'color': tier_color,
                                'fontWeight': 'bold',
                                'marginTop': '4px',
                                'display': 'inline-block'
                            }
                        )
                    ], style={'marginLeft': '16px', 'flex': '1'})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '16px'}),
                
                # Métricas principais
                html.Div([
                    # Seguidores
                    html.Div([
                        html.P('Seguidores', style={
                            'fontSize': '12px',
                            'color': '#9ca3af',
                            'margin': '0'
                        }),
                        html.H4(
                            f"{int(politico['followers']):,}",
                            style={
                                'fontSize': '24px',
                                'fontWeight': 'bold',
                                'color': '#fff',
                                'margin': '4px 0'
                            }
                        ),
                        html.Span([
                            html.Span(arrow_icon, style={'color': arrow_color, 'fontSize': '14px'}),
                            html.Span(
                                f" {abs(growth_7d):.1f}%",
                                style={'fontSize': '12px', 'color': arrow_color, 'marginLeft': '4px'}
                            )
                        ])
                    ], style={'flex': '1'}),
                    
                    # Engajamento
                    html.Div([
                        html.P('Engajamento', style={
                            'fontSize': '12px',
                            'color': '#9ca3af',
                            'margin': '0'
                        }),
                        html.H4(
                            f"{politico.get('avg_engagement_rate', 0):.2f}%",
                            style={
                                'fontSize': '24px',
                                'fontWeight': 'bold',
                                'color': '#fff',
                                'margin': '4px 0'
                            }
                        ),
                        html.P(
                            f"💬 {int(politico.get('avg_comments', 0)):,}",
                            style={'fontSize': '12px', 'color': '#9ca3af', 'margin': '4px 0 0 0'}
                        )
                    ], style={'flex': '1'})
                ], style={'display': 'flex', 'gap': '16px'})
            ])
        ], style={
            'backgroundColor': '#1f2937',
            'border': 'none',
            'borderRadius': '12px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'transition': 'transform 0.2s',
            'cursor': 'pointer',
            'height': '100%'
        }, id={'type': 'politico-card', 'username': politico['username']})
    ], style={'padding': '8px'}, className='col-12 col-md-6 col-lg-4 col-xl-3')


def create_radar_page(app):
    """Cria a página do Radar das Redes"""
    
    # Layout da página
    layout = html.Div([
        # Header
        html.Div([
            html.H2('🎯 Radar das Redes', style={
                'color': '#fff',
                'fontSize': '32px',
                'fontWeight': 'bold',
                'margin': '0'
            }),
            html.P('Monitoramento de políticos brasileiros no Instagram', style={
                'color': '#9ca3af',
                'fontSize': '16px',
                'margin': '8px 0 0 0'
            })
        ], style={
            'padding': '32px',
            'backgroundColor': '#111827',
            'borderBottom': '1px solid #374151'
        }),
        
        # Filtros
        html.Div([
            html.Div([
                html.Label('Filtrar por Tier:', style={'color': '#9ca3af', 'marginRight': '12px'}),
                dcc.Dropdown(
                    id='tier-filter',
                    options=[
                        {'label': 'Todos', 'value': 'all'},
                        {'label': '⭐ Tier 1 - Influência Máxima', 'value': 1},
                        {'label': '✨ Tier 2 - Alta Influência', 'value': 2},
                        {'label': '📍 Tier 3 - Regional/Temático', 'value': 3}
                    ],
                    value='all',
                    style={
                        'width': '300px',
                        'backgroundColor': '#1f2937',
                        'color': '#fff'
                    },
                    className='dark-dropdown'
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'}),
            
            html.Div([
                html.Label('Buscar:', style={'color': '#9ca3af', 'marginRight': '12px'}),
                dcc.Input(
                    id='search-input',
                    type='text',
                    placeholder='Nome, cargo ou partido...',
                    style={
                        'width': '300px',
                        'padding': '8px 12px',
                        'backgroundColor': '#1f2937',
                        'border': '1px solid #374151',
                        'borderRadius': '8px',
                        'color': '#fff'
                    }
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'})
        ], style={
            'padding': '24px 32px',
            'backgroundColor': '#111827',
            'display': 'flex',
            'justifyContent': 'space-between',
            'flexWrap': 'wrap',
            'gap': '16px'
        }),
        
        # Grid de cards
        html.Div(
            children=[create_politico_card(politico) for _, politico in get_politicos_data().iterrows()],
            id='politicos-grid', 
            className='row', 
            style={
                'padding': '24px',
                'backgroundColor': '#0f172a'
            }),
        
        # Modal para detalhes (futuro)
        html.Div(id='politico-modal')
        
    ], style={
        'minHeight': '100vh',
        'backgroundColor': '#0f172a'
    })
    
    # Callbacks
    @app.callback(
        Output('politicos-grid', 'children'),
        [Input('tier-filter', 'value'),
         Input('search-input', 'value')]
    )
    def update_grid(tier_filter, search_text):
        """Atualiza grid de políticos baseado nos filtros"""
        
        # Busca dados
        df = get_politicos_data()
        
        # Aplica filtro de tier
        if tier_filter != 'all':
            df = df[df['tier'] == tier_filter]
        
        # Aplica busca
        if search_text:
            search_text = search_text.lower()
            df = df[
                df['nome'].str.lower().str.contains(search_text) |
                df['cargo'].str.lower().str.contains(search_text) |
                df['partido'].str.lower().str.contains(search_text)
            ]
        
        # Cria cards
        if len(df) == 0:
            return html.Div([
                html.P('Nenhum político encontrado', style={
                    'color': '#9ca3af',
                    'textAlign': 'center',
                    'padding': '48px'
                })
            ])
        
        cards = []
        for idx, politico in df.iterrows():
            cards.append(create_politico_card(politico))
        
        return cards
    
    return layout


# CSS customizado para o dropdown escuro
app_css = '''
.dark-dropdown .Select-control {
    background-color: #1f2937 !important;
    border-color: #374151 !important;
    color: #fff !important;
}
.dark-dropdown .Select-menu-outer {
    background-color: #1f2937 !important;
    border-color: #374151 !important;
}
.dark-dropdown .Select-option {
    background-color: #1f2937 !important;
    color: #fff !important;
}
.dark-dropdown .Select-option:hover {
    background-color: #374151 !important;
}
'''
