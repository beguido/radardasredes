# 📊 Social Media Monitor - MVP Profissional

Sistema profissional de monitoramento de redes sociais com coleta automatizada via Apify e dashboards interativos.

## 🎯 Perfis Monitorados

### Principal
- @crismonteirosp

### Concorrentes/Referências
- @marinahelenabr
- @adriventurasp
- @leosiqueirabr

## 🛠️ Stack Tecnológica

- **Coleta**: Apify API (Instagram scraper)
- **Backend**: Python 3.9+
- **Banco**: SQLite (migração futura para PostgreSQL)
- **Dashboard**: Plotly Dash
- **Gráficos**: Plotly (interativos e profissionais)

## 📁 Estrutura do Projeto

```
social-monitor/
├── README.md
├── requirements.txt
├── config/
│   ├── settings.py          # Configurações centralizadas
│   └── apify_config.py      # Configuração Apify
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py      # Classe base
│   └── instagram_scraper.py # Scraper Instagram via Apify
├── database/
│   ├── __init__.py
│   ├── models.py            # Modelos de dados
│   └── db_manager.py        # Gerenciamento do banco
├── dashboard/
│   ├── __init__.py
│   ├── app.py               # Aplicação Dash principal
│   ├── components/
│   │   ├── __init__.py
│   │   ├── graphs.py        # Componentes de gráficos
│   │   └── layout.py        # Layout do dashboard
│   └── assets/
│       └── style.css        # Estilos customizados
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Funções auxiliares
└── scripts/
    ├── setup_database.py    # Setup inicial do banco
    ├── collect_data.py      # Script de coleta manual
    └── run_dashboard.py     # Iniciar dashboard
```

## 🚀 Setup Rápido (Mac)

### 1. Instalar Python (se não tiver)

```bash
# Verificar se Python está instalado
python3 --version

# Se não tiver, instalar via Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

### 2. Clonar/Baixar o projeto e instalar dependências

```bash
cd social-monitor
pip3 install -r requirements.txt
```

### 3. Criar conta Apify (GRATUITA)

1. Acesse: https://apify.com/sign-up
2. Crie conta gratuita ($5 em créditos grátis!)
3. Vá em: Settings → Integrations → API Token
4. Copie seu token

### 4. Configurar credenciais

Crie um arquivo `.env` na raiz do projeto:

```bash
# Copiar template
cp .env.example .env

# Editar e adicionar seu token
nano .env
```

Adicione:
```
APIFY_API_TOKEN=seu_token_aqui
```

### 5. Setup do banco de dados

```bash
python3 scripts/setup_database.py
```

### 6. Primeira coleta de dados

```bash
python3 scripts/collect_data.py
```

### 7. Iniciar dashboard

```bash
python3 scripts/run_dashboard.py
```

Acesse: http://localhost:8050

## 📊 Funcionalidades do Dashboard

### Gráficos Disponíveis

1. **Timeline de Crescimento**
   - Evolução de seguidores ao longo do tempo
   - Todas as contas em um único gráfico
   - Interativo (zoom, hover)

2. **Taxa de Crescimento**
   - Crescimento diário/semanal/mensal em %
   - Comparativo entre perfis

3. **Métricas Principais**
   - Tabela com dados atuais
   - Total de seguidores
   - Posts
   - Engajamento médio

4. **Análise Comparativa**
   - Benchmark entre perfis
   - Performance relativa

## 🔄 Automação

### Coleta Automática (Cron - Mac)

Editar crontab:
```bash
crontab -e
```

Adicionar (coleta diária às 9h):
```
0 9 * * * cd /caminho/para/social-monitor && python3 scripts/collect_data.py
```

## 💰 Custos Estimados

### Fase MVP (Atual)
- **Apify Free Tier**: $0/mês (suficiente para 4 perfis, coleta diária)
- **Hospedagem local**: $0/mês
- **Total**: $0/mês 🎉

### Fase de Crescimento
- **Apify Starter**: $49/mês (mais perfis, coletas frequentes)
- **VPS (DigitalOcean)**: $12/mês (para rodar 24/7)
- **Total**: ~$61/mês

## 🔐 Segurança

- ✅ Token Apify em variável de ambiente (.env)
- ✅ .env no .gitignore (nunca commitar credenciais)
- ✅ Banco de dados local (dados seguros)

## 📈 Roadmap Futuro

### Fase 2 - Automação Completa
- [ ] Deploy em VPS (DigitalOcean/AWS)
- [ ] Coleta automática via cron
- [ ] Notificações por email/Telegram
- [ ] Migração para PostgreSQL

### Fase 3 - Expansão
- [ ] YouTube, TikTok, Twitter
- [ ] Análise de posts individuais
- [ ] Análise de hashtags
- [ ] Previsão de crescimento (ML)

### Fase 4 - Profissional
- [ ] Multi-usuário
- [ ] API própria
- [ ] Relatórios automáticos PDF
- [ ] Integração com Google Analytics

## 🆘 Troubleshooting

### Erro: "Apify credits exhausted"
- Upgrade para plano pago ou aguarde reset mensal

### Dashboard não abre
- Verificar se porta 8050 está livre
- Verificar se banco tem dados

### Erro de importação
- Reinstalar dependências: `pip3 install -r requirements.txt`

## 📞 Suporte

Para dúvidas sobre:
- **Apify**: https://docs.apify.com
- **Plotly Dash**: https://dash.plotly.com
- **Python**: https://docs.python.org

---

**Desenvolvido com ❤️ para monitoramento profissional de @crismonteirosp**
