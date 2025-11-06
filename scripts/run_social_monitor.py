#!/usr/bin/env python3
"""
DASHBOARD COMPLETO - Social Monitor
- Radar da Cris (4 perfis principais)
- Radar das Redes (75+ políticos)
"""

import sys
sys.path.insert(0, '.')
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa app
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    suppress_callback_exceptions=True
)

server = app.server

# CSS Global
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Radar Social Monitor</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background-color: #0f172a;
            }
            * {
                box-sizing: border-box;
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

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                dbc.Col(html.Img(src="/assets/logo.png", height="30px"), width="auto"),
                dbc.Col(dbc.NavbarBrand("Social Monitor", className="ms-2")),
            ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"},
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("📊 Radar da Cris", href="/radar-cris", id="link-cris")),
                dbc.NavItem(dbc.NavLink("🎯 Radar das Redes", href="/radar-geral", id="link-geral")),
            ], className="ms-auto", navbar=True),
            id="navbar-collapse",
            is_open=False,
            navbar=True,
        ),
    ], fluid=True),
    color="dark",
    dark=True,
    sticky="top",
    style={'marginBottom': '0'}
)

# Layout principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


# Callback para navegação
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    # Por enquanto, sempre retorna Radar das Redes
    from scripts.radar_das_redes_page import create_radar_page
    return create_radar_page(app)


# Callback para toggle do navbar em mobile
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [Input("navbar-collapse", "is_open")]
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Callback para highlight do link ativo
@app.callback(
    [Output('link-cris', 'style'),
     Output('link-geral', 'style')],
    [Input('url', 'pathname')]
)
def update_active_link(pathname):
    active_style = {
        'backgroundColor': '#374151',
        'borderRadius': '6px'
    }
    inactive_style = {}
    
    if pathname == '/radar-geral':
        return inactive_style, active_style
    else:
        return active_style, inactive_style


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DASHBOARD_DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("🚀 SOCIAL MONITOR - Dashboard Completo")
    print("="*60)
    print(f"\n📊 Radar da Cris: http://127.0.0.1:{port}/")
    print(f"🎯 Radar das Redes: http://127.0.0.1:{port}/radar-geral")
    print(f"\n✨ Navegue entre as páginas usando o menu!")
    print("="*60 + "\n")
    
    app.run_server(host='0.0.0.0', port=port, debug=debug)
