"""
Aplicação principal do dashboard Plotly Dash
"""
from dash import Dash, callback, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd

from config import settings
from database import db
from dashboard.components import (
    get_layout, create_stats_cards,
    create_followers_timeline, create_growth_rate_chart,
    create_comparison_table, create_engagement_comparison
)
from scrapers import run_instagram_collection


# Inicializar app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Social Media Monitor",
    update_title=None,
    suppress_callback_exceptions=True
)

app.layout = get_layout()


# ==================== Callbacks ====================

@callback(
    [
        Output('stats-cards', 'children'),
        Output('followers-timeline-graph', 'figure'),
        Output('growth-rate-graph', 'figure'),
        Output('comparison-table-graph', 'figure'),
        Output('engagement-comparison-graph', 'figure'),
        Output('primary-profile-display', 'children'),
        Output('last-update-display', 'children'),
    ],
    [Input('period-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(period_days, n_intervals):
    """
    Atualiza todos os componentes do dashboard
    """
    # Carregar dados do banco
    df = db.get_instagram_dataframe(days=period_days)
    
    # Informações gerais
    primary_profile = f"⭐ @{settings.PRIMARY_PROFILE}"
    
    if df.empty:
        last_update = "Nenhum dado disponível"
        stats_cards = dbc.Alert(
            "Nenhum dado encontrado. Execute a coleta de dados primeiro!",
            color="warning",
            className="text-center"
        )
    else:
        last_update = df['collected_at'].max().strftime("%d/%m/%Y %H:%M")
        
        # Calcular estatísticas para cards
        latest_profiles = db.get_latest_instagram_profiles()
        
        total_followers = sum(p['followers'] for p in latest_profiles)
        primary_data = next(
            (p for p in latest_profiles if p['username'] == settings.PRIMARY_PROFILE),
            None
        )
        
        # Calcular crescimento total nos últimos 7 dias
        total_growth = 0
        for username in df['username'].unique():
            growth_data = db.calculate_growth(username, days=7)
            if growth_data:
                total_growth += growth_data['growth']
        
        # Criar cards de estatísticas
        stats_data = [
            {
                'title': 'Total de Seguidores',
                'value': f"{total_followers:,}",
                'subtitle': f'Todos os perfis',
                'color': '#3498db'
            },
            {
                'title': f'@{settings.PRIMARY_PROFILE}',
                'value': f"{primary_data['followers']:,}" if primary_data else 'N/A',
                'subtitle': 'Seguidores',
                'color': '#f39c12'
            },
            {
                'title': 'Crescimento 7 dias',
                'value': f"{total_growth:+,}",
                'subtitle': 'Todos os perfis',
                'color': '#27ae60' if total_growth >= 0 else '#e74c3c'
            },
            {
                'title': 'Perfis Monitorados',
                'value': str(len(latest_profiles)),
                'subtitle': f'Última coleta: {last_update}',
                'color': '#9b59b6'
            }
        ]
        
        stats_cards = create_stats_cards(stats_data)
    
    # Criar gráficos
    timeline_fig = create_followers_timeline(df)
    growth_fig = create_growth_rate_chart(df, period_days=7)
    table_fig = create_comparison_table(df)
    engagement_fig = create_engagement_comparison(df)
    
    return (
        stats_cards,
        timeline_fig,
        growth_fig,
        table_fig,
        engagement_fig,
        primary_profile,
        last_update
    )


@callback(
    Output('refresh-status', 'children'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=True
)
def trigger_data_collection(n_clicks):
    """
    Trigger para coleta manual de dados
    """
    if n_clicks:
        try:
            # Executar coleta
            results = run_instagram_collection()
            
            if results:
                return dbc.Alert(
                    f"✅ Coleta concluída! {len(results)} perfis atualizados.",
                    color="success",
                    dismissable=True,
                    duration=5000
                )
            else:
                return dbc.Alert(
                    "⚠️ Nenhum dado foi coletado. Verifique os logs.",
                    color="warning",
                    dismissable=True,
                    duration=5000
                )
                
        except Exception as e:
            return dbc.Alert(
                f"❌ Erro na coleta: {str(e)}",
                color="danger",
                dismissable=True,
                duration=5000
            )
    
    return ""


def run_server(host=None, port=None, debug=None):
    """
    Inicializa o servidor do dashboard
    """
    host = host or settings.DASHBOARD_HOST
    port = port or settings.DASHBOARD_PORT
    debug = debug if debug is not None else settings.DASHBOARD_DEBUG
    
    print("\n" + "="*60)
    print("🚀 INICIANDO DASHBOARD")
    print("="*60)
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Modo Debug: {debug}")
    print(f"⭐ Perfil Principal: @{settings.PRIMARY_PROFILE}")
    print(f"📊 Perfis Monitorados: {len(settings.INSTAGRAM_PROFILES)}")
    print("="*60)
    print("\n💡 Dica: Pressione Ctrl+C para parar o servidor\n")
    
    app.run_server(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
