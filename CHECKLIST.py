"""
✅ CHECKLIST DE SETUP
====================

Use este checklist para garantir que tudo está configurado corretamente.
"""

CHECKLIST = """
📋 CHECKLIST COMPLETO - SOCIAL MEDIA MONITOR
============================================

PRÉ-REQUISITOS
─────────────
[ ] Mac OS X (10.14 ou superior)
[ ] Conexão com internet
[ ] Conta Google ou GitHub (para Apify)
[ ] Navegador atualizado (Chrome, Firefox, Safari)

PASSO 1: PYTHON
───────────────
[ ] Python 3.9+ instalado
    Verificar: python3 --version
    
[ ] pip atualizado
    Atualizar: pip3 install --upgrade pip

PASSO 2: PROJETO
────────────────
[ ] Projeto baixado/extraído
[ ] Terminal aberto na pasta do projeto
    cd /caminho/para/social-monitor

PASSO 3: DEPENDÊNCIAS
─────────────────────
[ ] requirements.txt presente
[ ] Dependências instaladas
    Comando: pip3 install -r requirements.txt
    
[ ] Verificar instalação:
    python3 -c "import dash; import plotly; import apify_client; print('✅ OK')"

PASSO 4: CONTA APIFY
────────────────────
[ ] Conta criada em https://apify.com/sign-up
[ ] Email verificado
[ ] $5 em créditos gratuitos creditados
[ ] Token API copiado (Settings → Integrations)

PASSO 5: CONFIGURAÇÃO
─────────────────────
[ ] Arquivo .env criado
    Comando: cp .env.example .env
    
[ ] Token Apify adicionado ao .env
    APIFY_API_TOKEN=apify_api_seu_token_aqui
    
[ ] Perfis configurados (se necessário alterar)
    INSTAGRAM_PROFILES=crismonteirosp,marinahelenabr,adriventurasp,leosiqueirabr

PASSO 6: BANCO DE DADOS
────────────────────────
[ ] Pasta data/ criada automaticamente
[ ] Banco de dados criado
    Comando: python3 scripts/setup_database.py
    
[ ] Tabelas criadas com sucesso
    ✓ instagram_profiles
    ✓ collection_logs
    ✓ daily_metrics

PASSO 7: PRIMEIRA COLETA
─────────────────────────
[ ] Script de coleta executado
    Comando: python3 scripts/collect_data.py
    
[ ] 4 perfis coletados com sucesso
    ✓ @crismonteirosp
    ✓ @marinahelenabr
    ✓ @adriventurasp
    ✓ @leosiqueirabr
    
[ ] Dados salvos no banco (verificar logs)

PASSO 8: DASHBOARD
──────────────────
[ ] Dashboard iniciado
    Comando: python3 scripts/run_dashboard.py
    
[ ] Servidor rodando na porta 8050
[ ] Navegador aberto em http://localhost:8050
[ ] Gráficos carregando corretamente
[ ] Dados visíveis em todos os componentes

VERIFICAÇÃO FINAL
─────────────────
[ ] Timeline de seguidores funciona
[ ] Gráfico de crescimento funciona
[ ] Tabela comparativa funciona
[ ] Filtro de período funciona
[ ] Botão "Coletar Novos Dados" funciona

TESTES ADICIONAIS
─────────────────
[ ] Trocar período de análise (7, 15, 30 dias)
[ ] Zoom em gráficos funciona
[ ] Hover mostra informações corretas
[ ] Exportar gráfico (câmera no canto)
[ ] Dashboard responsivo (redimensionar janela)

DOCUMENTAÇÃO LIDA
─────────────────
[ ] README.md lido
[ ] QUICKSTART.py consultado
[ ] ARCHITECTURE.md revisado (opcional)
[ ] TROUBLESHOOTING.py marcado (para referência)

PRÓXIMOS PASSOS
───────────────
[ ] Configurar coleta automática (cron)
[ ] Adicionar mais perfis (se necessário)
[ ] Explorar ADVANCED_EXAMPLES.py
[ ] Planejar deploy em servidor (futuro)

BACKUP E SEGURANÇA
──────────────────
[ ] .env no .gitignore (não commitar!)
[ ] Backup inicial do banco criado
    cp data/social_monitor.db backup/inicial.db
[ ] Documentar senha/token em local seguro

SUPORTE
───────
[ ] Bookmarks salvos:
    • https://docs.apify.com
    • https://dash.plotly.com
    • https://docs.sqlalchemy.org
    
[ ] TROUBLESHOOTING.py marcado para consulta
[ ] Contato de suporte identificado (se houver)

═══════════════════════════════════════════════

✅ SE TODOS OS ITENS ESTÃO MARCADOS:
   PARABÉNS! Seu Social Media Monitor está 100% funcional!

⚠️  SE ALGO NÃO FUNCIONOU:
   Consulte TROUBLESHOOTING.py para soluções

═══════════════════════════════════════════════
"""

def print_checklist():
    print(CHECKLIST)

def verify_setup():
    """
    Script para verificar automaticamente o setup
    """
    import sys
    import os
    from pathlib import Path
    
    print("\n🔍 VERIFICANDO SETUP AUTOMÁTICO...\n")
    
    checks = []
    
    # Check 1: Python version
    import sys
    python_version = sys.version_info
    if python_version >= (3, 9):
        checks.append(("✅", "Python 3.9+"))
    else:
        checks.append(("❌", f"Python {python_version.major}.{python_version.minor} (precisa 3.9+)"))
    
    # Check 2: Dependencies
    try:
        import dash
        import plotly
        import apify_client
        import sqlalchemy
        import pandas
        checks.append(("✅", "Todas as dependências instaladas"))
    except ImportError as e:
        checks.append(("❌", f"Dependência faltando: {e.name}"))
    
    # Check 3: .env file
    if Path(".env").exists():
        checks.append(("✅", "Arquivo .env existe"))
        
        # Check token
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv("APIFY_API_TOKEN")
        if token and token.startswith("apify_api_"):
            checks.append(("✅", "Token Apify configurado"))
        else:
            checks.append(("⚠️ ", "Token Apify não configurado ou inválido"))
    else:
        checks.append(("❌", "Arquivo .env não encontrado"))
    
    # Check 4: Database
    if Path("data/social_monitor.db").exists():
        checks.append(("✅", "Banco de dados existe"))
        
        # Check tables
        try:
            from database import db
            with db.get_session() as session:
                result = session.execute("SELECT COUNT(*) FROM instagram_profiles")
                count = result.scalar()
                checks.append(("✅", f"Banco operacional ({count} registros)"))
        except Exception as e:
            checks.append(("⚠️ ", f"Problema no banco: {str(e)[:50]}"))
    else:
        checks.append(("❌", "Banco de dados não criado"))
    
    # Print results
    print("═" * 60)
    for status, message in checks:
        print(f"{status} {message}")
    print("═" * 60)
    
    # Summary
    success_count = sum(1 for status, _ in checks if status == "✅")
    total_count = len(checks)
    
    print(f"\n📊 Status: {success_count}/{total_count} verificações passaram")
    
    if success_count == total_count:
        print("🎉 TUDO CERTO! Sistema 100% funcional!\n")
        return True
    else:
        print("⚠️  Alguns problemas encontrados. Consulte TROUBLESHOOTING.py\n")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_setup()
    else:
        print_checklist()
