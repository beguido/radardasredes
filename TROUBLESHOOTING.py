"""
🔧 GUIA DE TROUBLESHOOTING
==========================

Soluções para problemas comuns que você pode encontrar.
"""

# ==================== PROBLEMAS DE INSTALAÇÃO ====================

"""
❌ ERRO: "pip3: command not found"
───────────────────────────────────

SOLUÇÃO:
Python não está instalado ou não está no PATH.

1. Instalar Python via Homebrew:
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python

2. Ou baixar de: https://www.python.org/downloads/
"""

"""
❌ ERRO: "permission denied" ao instalar dependências
──────────────────────────────────────────────────────

SOLUÇÃO:
Use --user ou sudo (não recomendado).

Preferível:
pip3 install --user -r requirements.txt

Ou criar ambiente virtual:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
"""

"""
❌ ERRO: Módulo não encontrado após instalação
───────────────────────────────────────────────

SOLUÇÃO:
Você pode ter múltiplas versões de Python.

1. Verificar qual Python está usando:
   which python3
   python3 --version

2. Instalar no Python correto:
   python3 -m pip install -r requirements.txt
"""

# ==================== PROBLEMAS DE CONFIGURAÇÃO ====================

"""
❌ ERRO: "APIFY_API_TOKEN não configurado no arquivo .env"
──────────────────────────────────────────────────────────

SOLUÇÃO:
O arquivo .env não existe ou está mal configurado.

1. Criar .env a partir do template:
   cp .env.example .env

2. Editar .env:
   nano .env
   
3. Adicionar seu token:
   APIFY_API_TOKEN=apify_api_seu_token_aqui
   
4. Salvar (Ctrl+O, Enter, Ctrl+X)

⚠️  IMPORTANTE: Token deve começar com "apify_api_"
"""

"""
❌ ERRO: "Invalid Apify token"
──────────────────────────────

SOLUÇÃO:
Token incorreto ou expirado.

1. Pegar token correto:
   - Login em https://apify.com
   - Settings → Integrations
   - Copiar "Personal API Token"

2. Verificar se não tem espaços extras:
   APIFY_API_TOKEN=apify_api_xxxxx  ← CORRETO
   APIFY_API_TOKEN= apify_api_xxxxx ← ERRADO (espaço)
"""

# ==================== PROBLEMAS DE COLETA ====================

"""
❌ ERRO: "Nenhum dado encontrado para @username"
────────────────────────────────────────────────

POSSÍVEIS CAUSAS:
1. Username errado (typo)
2. Perfil privado
3. Perfil foi deletado/suspenso
4. Rate limit do Instagram

SOLUÇÃO:
1. Verificar se username está correto (sem @):
   INSTAGRAM_PROFILES=crismonteirosp,marinahelenabr

2. Verificar se perfil é público:
   Abra no navegador: instagram.com/username

3. Aguardar alguns minutos e tentar novamente
"""

"""
❌ ERRO: "Apify credits exhausted"
──────────────────────────────────

SOLUÇÃO:
Você gastou todos os créditos gratuitos.

Opções:
1. Aguardar reset mensal (todo dia 1º)
2. Upgrade para plano pago:
   - Starter: $49/mês
   - Scale: $499/mês

Consumo estimado:
- 1 perfil = ~$0.10
- 4 perfis/dia = ~$12/mês
"""

"""
❌ ERRO: Timeout durante coleta
────────────────────────────────

SOLUÇÃO:
Instagram está lento ou Apify está congestionado.

1. Aumentar timeout em config/settings.py:
   COLLECTION_SETTINGS = {
       "timeout": 600,  # 10 minutos
   }

2. Tentar novamente mais tarde
"""

# ==================== PROBLEMAS DO DASHBOARD ====================

"""
❌ ERRO: "Address already in use" (porta 8050)
──────────────────────────────────────────────

SOLUÇÃO:
Já tem um dashboard rodando.

1. Encontrar processo:
   lsof -ti:8050

2. Matar processo:
   kill -9 $(lsof -ti:8050)

Ou mudar porta em .env:
DASHBOARD_PORT=8051
"""

"""
❌ ERRO: Dashboard abre mas mostra "Nenhum dado disponível"
───────────────────────────────────────────────────────────

SOLUÇÃO:
Você ainda não coletou dados.

1. Executar coleta:
   python3 scripts/collect_data.py

2. Recarregar dashboard (F5)
"""

"""
❌ ERRO: Gráficos não aparecem / Dashboard em branco
────────────────────────────────────────────────────

POSSÍVEIS CAUSAS:
1. JavaScript desabilitado no navegador
2. Extensão de ad-blocker interferindo
3. Problema de cache

SOLUÇÃO:
1. Limpar cache do navegador (Cmd+Shift+R)
2. Tentar em modo anônimo
3. Desabilitar ad-blockers temporariamente
4. Tentar outro navegador (Chrome, Firefox, Safari)
"""

# ==================== PROBLEMAS DO BANCO DE DADOS ====================

"""
❌ ERRO: "database is locked"
─────────────────────────────

SOLUÇÃO:
Outro processo está usando o banco.

1. Verificar se coleta está rodando
2. Fechar todos os scripts Python
3. Reiniciar dashboard

Se persistir:
rm data/social_monitor.db
python3 scripts/setup_database.py
python3 scripts/collect_data.py
"""

"""
❌ ERRO: Dados duplicados ou inconsistentes
───────────────────────────────────────────

SOLUÇÃO:
Problema na coleta ou banco corrompido.

1. Backup do banco atual:
   cp data/social_monitor.db data/social_monitor.db.backup

2. Recriar banco limpo:
   rm data/social_monitor.db
   python3 scripts/setup_database.py

3. Coletar dados novamente:
   python3 scripts/collect_data.py
"""

# ==================== PROBLEMAS DE PERFORMANCE ====================

"""
❌ PROBLEMA: Dashboard muito lento
──────────────────────────────────

SOLUÇÃO:
Muito dados acumulados no banco.

1. Limitar período de análise:
   - Use filtro "Últimos 30 dias"
   - Não use "Últimos 365 dias"

2. Limpar dados antigos (se necessário):
   # Via Python console
   from database import db
   # Deletar dados > 6 meses
   # (código customizado)
"""

"""
❌ PROBLEMA: Coleta muito demorada
──────────────────────────────────

SOLUÇÃO:
Muitos perfis ou timeout alto.

1. Reduzir perfis monitorados
2. Ajustar wait_between_profiles em config/settings.py:
   "wait_between_profiles": 1,  # Reduzir de 2 para 1
"""

# ==================== DICAS DE DEBUG ====================

"""
🐛 COMO DEBUGAR PROBLEMAS

1. Ativar modo debug no dashboard:
   DASHBOARD_DEBUG=True  (no .env)

2. Ver logs detalhados:
   python3 scripts/collect_data.py 2>&1 | tee logs.txt

3. Testar conexão Apify:
   from apify_client import ApifyClient
   client = ApifyClient("seu_token")
   user = client.user().get()
   print(user)

4. Verificar banco de dados:
   sqlite3 data/social_monitor.db
   .tables
   SELECT COUNT(*) FROM instagram_profiles;
   .quit

5. Ver últimos logs de coleta:
   from database import db
   logs = db.get_collection_logs(limit=10)
   for log in logs:
       print(log)
"""

# ==================== RECUPERAÇÃO DE DESASTRES ====================

"""
💾 BACKUP E RECUPERAÇÃO

FAZER BACKUP:
1. Backup manual:
   cp data/social_monitor.db backup/social_monitor_$(date +%Y%m%d).db

2. Backup automático (cron):
   0 3 * * * cp /path/social_monitor.db /path/backup/db_$(date +\%Y\%m\%d).db

RESTAURAR BACKUP:
1. Parar dashboard
2. Restaurar banco:
   cp backup/social_monitor_20241029.db data/social_monitor.db
3. Reiniciar dashboard
"""

# ==================== CONTATOS E RECURSOS ====================

"""
📚 RECURSOS ÚTEIS

Documentação:
- Apify: https://docs.apify.com
- Plotly Dash: https://dash.plotly.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Pandas: https://pandas.pydata.org

Comunidades:
- Stack Overflow: https://stackoverflow.com
- Reddit: r/learnpython, r/datascience
- Discord: Python Discord, Data Science Discord

APIs Úteis:
- Apify Store: https://apify.com/store
- Instagram Graph API: https://developers.facebook.com/docs/instagram-api

Ferramentas Alternativas:
- Metricool
- Hootsuite
- Sprout Social
- Buffer
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n✅ Este arquivo contém soluções para problemas comuns.")
    print("📖 Leia com atenção quando encontrar algum erro.\n")
