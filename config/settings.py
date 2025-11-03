"""
Configurações centralizadas do projeto
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Apify
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN não configurado no arquivo .env")

# IDs dos scrapers Apify (oficiais)
APIFY_INSTAGRAM_SCRAPER = "apify/instagram-profile-scraper"

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "social_monitor.db"))

# Dashboard
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "127.0.0.1")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8050"))
DASHBOARD_DEBUG = os.getenv("DASHBOARD_DEBUG", "True").lower() == "true"

# Perfis para monitorar
INSTAGRAM_PROFILES = os.getenv(
    "INSTAGRAM_PROFILES",
    "crismonteirosp,marinahelenabr,adriventurasp,leosiqueirabr"
).split(",")

# Configurações de coleta
COLLECTION_SETTINGS = {
    "max_retries": 3,
    "timeout": 300,  # 5 minutos
    "wait_between_profiles": 2,  # segundos
}

# Configurações do dashboard
DASHBOARD_SETTINGS = {
    "refresh_interval": 3600,  # 1 hora em segundos
    "theme": "plotly_white",
    "color_scheme": [
        "#1f77b4",  # azul
        "#ff7f0e",  # laranja
        "#2ca02c",  # verde
        "#d62728",  # vermelho
    ],
}

# Perfil principal (destaque)
PRIMARY_PROFILE = "crismonteirosp"
