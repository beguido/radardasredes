"""
🚀 GUIA RÁPIDO DE INÍCIO
========================

Siga estes passos para colocar o Social Media Monitor funcionando:

PASSO 1: INSTALAR PYTHON
-------------------------
Mac vem com Python, mas vamos garantir que está atualizado:

1. Abra o Terminal (Cmd + Espaço, digite "Terminal")

2. Verifique se tem Python:
   python3 --version

3. Se não tiver ou estiver desatualizado, instale via Homebrew:
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python


PASSO 2: INSTALAR DEPENDÊNCIAS
-------------------------------
No Terminal, navegue até a pasta do projeto:

cd /caminho/para/social-monitor

Instale as bibliotecas necessárias:

pip3 install -r requirements.txt

Isso vai instalar:
✓ Apify Client (para coleta de dados)
✓ SQLAlchemy (banco de dados)
✓ Plotly Dash (dashboard interativo)
✓ Pandas (análise de dados)
✓ E outras dependências


PASSO 3: CRIAR CONTA APIFY (GRÁTIS!)
-------------------------------------
1. Acesse: https://apify.com/sign-up

2. Crie sua conta (use Google/GitHub para facilitar)

3. Você ganha $5 em créditos gratuitos! 🎉
   Suficiente para ~10.000 páginas scraped

4. Pegue seu API Token:
   - Clique no seu avatar (canto superior direito)
   - Settings → Integrations
   - Copie o "Personal API Token"


PASSO 4: CONFIGURAR O PROJETO
------------------------------
1. Crie o arquivo de configuração:
   
   cp .env.example .env

2. Abra o arquivo .env em um editor de texto:
   
   nano .env
   
   Ou use TextEdit/VSCode

3. Cole seu token Apify:
   
   APIFY_API_TOKEN=seu_token_aqui_colado

4. Salve o arquivo (Ctrl+O, Enter, Ctrl+X se estiver usando nano)


PASSO 5: CONFIGURAR BANCO DE DADOS
-----------------------------------
Execute o script de setup:

python3 scripts/setup_database.py

Isso vai criar:
✓ Pasta data/
✓ Banco SQLite com todas as tabelas
✓ Estrutura pronta para receber dados


PASSO 6: PRIMEIRA COLETA DE DADOS! 🎯
--------------------------------------
Agora vamos buscar os dados do Instagram:

python3 scripts/collect_data.py

O que vai acontecer:
1. Conecta com Apify
2. Busca dados de cada perfil (@crismonteirosp, @marinahelenabr, etc)
3. Salva tudo no banco de dados

Tempo estimado: 2-3 minutos

⚠️  IMPORTANTE: Isso consome créditos Apify (~$0.10 por perfil)


PASSO 7: ABRIR O DASHBOARD! 🎨
-------------------------------
Inicie o dashboard:

python3 scripts/run_dashboard.py

Abra seu navegador em:
http://localhost:8050

Você verá:
✨ Gráficos interativos de crescimento
📊 Comparativos entre perfis
📈 Taxa de engajamento
📋 Tabela com todas as métricas


DICAS IMPORTANTES
-----------------

💡 Coletar dados diariamente:
   Execute o script collect_data.py todo dia no mesmo horário

💡 Automatizar coleta (Mac):
   Use cron para rodar automaticamente:
   
   crontab -e
   
   Adicione (coleta todo dia às 9h):
   0 9 * * * cd /caminho/para/social-monitor && python3 scripts/collect_data.py

💡 Custos Apify:
   - Free tier: $5/mês (suficiente para teste)
   - 4 perfis, 1x por dia = ~$12/mês de consumo
   - Plano Starter ($49/mês) recomendado para uso regular

💡 Ver logs de coleta:
   O banco guarda histórico de todas as coletas na tabela collection_logs


PROBLEMAS COMUNS
----------------

❌ "APIFY_API_TOKEN não configurado"
→ Você não configurou o arquivo .env corretamente

❌ "Nenhum dado encontrado"
→ Username pode estar errado ou perfil privado

❌ "Port 8050 already in use"
→ Já tem um dashboard rodando, feche e tente novamente

❌ "Module not found"
→ Não instalou as dependências: pip3 install -r requirements.txt


PRÓXIMOS PASSOS
---------------

Fase 2 - Melhorias:
□ Deploy em servidor (DigitalOcean, AWS)
□ Adicionar YouTube, TikTok
□ Notificações por email
□ Análise de hashtags
□ Previsões com Machine Learning

Fase 3 - Profissional:
□ Multi-usuário
□ API própria
□ Relatórios PDF automáticos
□ Integração com Google Analytics


SUPORTE
-------

Dúvidas sobre Apify:
→ https://docs.apify.com

Dúvidas sobre Plotly:
→ https://dash.plotly.com

Documentação Python:
→ https://docs.python.org


BOA SORTE! 🚀

Desenvolvido com ❤️ para @crismonteirosp
"""

if __name__ == "__main__":
    print(__doc__)
