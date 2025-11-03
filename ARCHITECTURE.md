# 🏗️ ARQUITETURA DO SISTEMA

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                     SOCIAL MEDIA MONITOR                         │
│            Sistema Profissional de Monitoramento                 │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│   INSTAGRAM  │────────│   APIFY API  │────────│    PYTHON    │
│   (Dados)    │        │  (Scraping)  │        │  (Backend)   │
└──────────────┘        └──────────────┘        └──────┬───────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  SQLite / DB    │
                                              │  (Armazenamento)│
                                              └────────┬────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  PLOTLY DASH    │
                                              │  (Dashboard)    │
                                              └────────┬────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   NAVEGADOR     │
                                              │ (localhost:8050)│
                                              └─────────────────┘
```

## Componentes Principais

### 1. CAMADA DE COLETA (Scrapers)

**Arquivo:** `scrapers/instagram_scraper.py`

**Responsabilidades:**
- Conectar com Apify API
- Enviar requisições de scraping
- Processar dados retornados
- Calcular métricas de engajamento
- Gerenciar rate limiting

**Fluxo:**
```python
1. InstagramScraper.scrape_profile(username)
   ↓
2. Apify Actor: instagram-profile-scraper
   ↓
3. Retorno: JSON com dados do perfil
   ↓
4. Enriquecimento: cálculo de engagement_rate
   ↓
5. Salvamento no banco de dados
```

**Dados Coletados:**
- username
- full_name
- biography
- followers
- following
- posts_count
- is_verified
- is_business
- engagement_rate (calculado)
- avg_likes (calculado)
- avg_comments (calculado)

---

### 2. CAMADA DE DADOS (Database)

**Arquivos:**
- `database/models.py` - Definição das tabelas
- `database/db_manager.py` - Operações CRUD

**Tabelas:**

#### 📊 instagram_profiles
Armazena snapshots de perfis ao longo do tempo
```
id              INTEGER PRIMARY KEY
username        VARCHAR(100)
full_name       VARCHAR(200)
biography       TEXT
followers       INTEGER
following       INTEGER
posts_count     INTEGER
is_verified     BOOLEAN
is_business     BOOLEAN
engagement_rate FLOAT
collected_at    DATETIME
is_primary      BOOLEAN
```

#### 📝 collection_logs
Log de todas as coletas realizadas
```
id                INTEGER PRIMARY KEY
platform          VARCHAR(50)
username          VARCHAR(100)
status            VARCHAR(20)
error_message     TEXT
records_collected INTEGER
execution_time    FLOAT
collected_at      DATETIME
```

#### 📈 daily_metrics
Métricas consolidadas por dia (otimização)
```
id                  INTEGER PRIMARY KEY
platform            VARCHAR(50)
username            VARCHAR(100)
date                DATETIME
followers           INTEGER
followers_growth    INTEGER
followers_growth_rate FLOAT
engagement_rate     FLOAT
```

**Operações Principais:**
- `save_instagram_profile()` - Salvar novo snapshot
- `get_instagram_history()` - Histórico de um perfil
- `get_latest_instagram_profiles()` - Dados mais recentes
- `calculate_growth()` - Calcular crescimento
- `get_instagram_dataframe()` - Dados em formato Pandas

---

### 3. CAMADA DE VISUALIZAÇÃO (Dashboard)

**Arquivos:**
- `dashboard/app.py` - Aplicação Dash principal
- `dashboard/components/graphs.py` - Componentes de gráficos
- `dashboard/components/layout.py` - Layout do dashboard

**Componentes Visuais:**

#### 📈 Gráfico de Timeline
```python
create_followers_timeline(df)
```
- Gráfico de linhas interativo
- Mostra evolução de seguidores ao longo do tempo
- Múltiplos perfis no mesmo gráfico
- Destaque para perfil principal

#### 📊 Taxa de Crescimento
```python
create_growth_rate_chart(df, period_days=7)
```
- Gráfico de barras
- Mostra % de crescimento
- Cores: verde (positivo), vermelho (negativo)

#### 📋 Tabela Comparativa
```python
create_comparison_table(df)
```
- Tabela com todas as métricas
- Seguidores, posts, engajamento
- Crescimento últimos 7 dias

#### 💬 Comparativo de Engajamento
```python
create_engagement_comparison(df)
```
- Barras horizontais
- Compara taxa de engajamento entre perfis

**Callbacks (Interatividade):**
```python
@callback(
    [Output(...)],
    [Input('period-dropdown', 'value')]
)
def update_dashboard(period_days):
    # Atualiza todos os gráficos quando mudar período
```

---

### 4. CAMADA DE CONFIGURAÇÃO (Config)

**Arquivo:** `config/settings.py`

**Variáveis de Ambiente (.env):**
```bash
APIFY_API_TOKEN=apify_api_xxxxx
DATABASE_PATH=data/social_monitor.db
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=8050
INSTAGRAM_PROFILES=crismonteirosp,marinahelenabr,adriventurasp,leosiqueirabr
```

**Configurações:**
- APIFY_API_TOKEN - Token de autenticação
- INSTAGRAM_PROFILES - Lista de perfis
- PRIMARY_PROFILE - Perfil principal (destaque)
- COLLECTION_SETTINGS - Timeout, retries
- DASHBOARD_SETTINGS - Cores, tema

---

## Fluxo Completo de Dados

### 🔄 Coleta de Dados

```
1. Usuário executa: python3 scripts/collect_data.py
   ↓
2. InstagramScraper inicia
   ↓
3. Para cada username em INSTAGRAM_PROFILES:
   ├─ Chama Apify API
   ├─ Aguarda resposta (timeout: 300s)
   ├─ Processa dados
   ├─ Calcula métricas
   ├─ Salva no banco
   └─ Aguarda 2s (rate limiting)
   ↓
4. Retorna summary de coleta
```

### 📊 Visualização

```
1. Usuário executa: python3 scripts/run_dashboard.py
   ↓
2. Dashboard Dash inicia na porta 8050
   ↓
3. Usuário acessa: http://localhost:8050
   ↓
4. Callback carrega dados do banco
   ↓
5. Gráficos são renderizados
   ↓
6. Usuário interage (filtros, zoom, hover)
   ↓
7. Callbacks atualizam visualizações
```

---

## Padrões de Projeto Utilizados

### 1. **Repository Pattern** (database/db_manager.py)
- Encapsula lógica de acesso a dados
- Abstração sobre SQLAlchemy
- Facilita testes e manutenção

### 2. **Factory Pattern** (dashboard/components/graphs.py)
- Funções factory para criar gráficos
- Padronização de estilos
- Reutilização de código

### 3. **Singleton Pattern** (database/db_manager.py)
- Instância única do DatabaseManager
- Reuso de conexões
- Gerenciamento centralizado

### 4. **Strategy Pattern** (scrapers/)
- Diferentes estratégias de scraping
- Fácil adicionar novas redes sociais
- Base abstrata para scrapers

---

## Escalabilidade

### Fase Atual (MVP)
- SQLite (banco local)
- Coleta manual
- 1 usuário
- Hospedagem local

### Fase 2 (Crescimento)
```
┌─────────────┐
│   USUÁRIO   │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│  VPS/Cloud   │
│ (DigitalOcean│
│  ou AWS)     │
└──────┬───────┘
       │
       ├─────► PostgreSQL (banco)
       ├─────► Redis (cache)
       └─────► Cron (automação)
```

### Fase 3 (Enterprise)
```
┌──────────────────────────────────────┐
│         Load Balancer (Nginx)         │
└───────────────┬──────────────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│ App 1  │ │ App 2  │ │ App 3  │
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    └──────────┼──────────┘
               ▼
      ┌────────────────┐
      │   PostgreSQL   │
      │   (Primary)    │
      └────────┬───────┘
               │
               ▼
      ┌────────────────┐
      │   PostgreSQL   │
      │   (Replica)    │
      └────────────────┘
```

---

## Performance

### Otimizações Implementadas

1. **Índices de Banco:**
```sql
CREATE INDEX idx_username_date ON instagram_profiles(username, collected_at);
CREATE INDEX idx_username_platform_date ON daily_metrics(username, platform, date);
```

2. **Cache de Queries:**
- Uso de Pandas para agregações em memória
- Queries otimizadas com SQLAlchemy

3. **Lazy Loading:**
- Gráficos carregam apenas dados do período selecionado
- Paginação em queries grandes

4. **Rate Limiting:**
- Delay de 2s entre coletas
- Previne bloqueios do Instagram/Apify

---

## Segurança

### Medidas Implementadas

✅ **Credenciais em .env**
- Nunca commitar .env
- .gitignore configurado

✅ **Validação de Inputs**
- Validação de usernames
- Sanitização de dados

✅ **Logs de Auditoria**
- Todas as coletas são logadas
- Rastreabilidade completa

✅ **Backup**
- Recomendação de backup diário
- Scripts de recuperação

### TODO (Segurança Futura)

- [ ] Criptografia de dados sensíveis
- [ ] Autenticação multi-fator
- [ ] API rate limiting
- [ ] Monitoramento de anomalias

---

## Monitoramento

### Métricas a Monitorar

1. **Saúde do Sistema:**
   - Taxa de sucesso das coletas
   - Tempo médio de coleta
   - Erros e exceções

2. **Qualidade dos Dados:**
   - Dados faltantes
   - Outliers e anomalias
   - Consistência temporal

3. **Performance:**
   - Tempo de resposta do dashboard
   - Uso de memória
   - Tamanho do banco

### Ferramentas Recomendadas

- **Uptime**: UptimeRobot (free)
- **Logs**: Loguru ou Sentry
- **Métricas**: Prometheus + Grafana
- **Alertas**: Telegram Bot / Email

---

## Testes

### Estrutura de Testes (TODO)

```
tests/
├── test_scrapers.py
│   ├── test_instagram_scraper
│   └── test_error_handling
├── test_database.py
│   ├── test_save_profile
│   ├── test_calculate_growth
│   └── test_queries
└── test_dashboard.py
    ├── test_graph_creation
    └── test_callbacks
```

### Comandos
```bash
# Instalar pytest
pip install pytest

# Rodar testes
pytest tests/

# Com cobertura
pytest --cov=. tests/
```

---

## Documentação de API

### DatabaseManager

```python
# Salvar perfil
db.save_instagram_profile(profile_data, is_primary=True)

# Histórico
history = db.get_instagram_history(username='crismonteirosp', days=30)

# Calcular crescimento
growth = db.calculate_growth(username='crismonteirosp', days=7)

# DataFrame para análises
df = db.get_instagram_dataframe(days=90)
```

### InstagramScraper

```python
# Instanciar
scraper = InstagramScraper(api_token='apify_api_xxx')

# Coletar um perfil
data = scraper.scrape_profile('crismonteirosp')

# Coletar múltiplos
results = scraper.scrape_multiple_profiles(
    usernames=['crismonteirosp', 'marinahelenabr'],
    primary_username='crismonteirosp'
)
```

---

## Manutenção

### Tarefas Regulares

**Diárias:**
- ✅ Executar coleta de dados
- ✅ Verificar logs de erro

**Semanais:**
- ✅ Revisar crescimento
- ✅ Backup do banco de dados

**Mensais:**
- ✅ Análise de custos Apify
- ✅ Atualizar dependências
- ✅ Limpar dados antigos (opcional)

**Trimestrais:**
- ✅ Revisar e otimizar queries
- ✅ Atualizar documentação
- ✅ Planejar novas features

---

## Roadmap Técnico

### Q1 2025
- [ ] Migração para PostgreSQL
- [ ] Deploy em VPS
- [ ] Automação de coleta (cron)
- [ ] Sistema de alertas

### Q2 2025
- [ ] Adicionar YouTube e TikTok
- [ ] Dashboard mobile responsivo
- [ ] Exportação de relatórios PDF
- [ ] API REST

### Q3 2025
- [ ] Machine Learning (previsões)
- [ ] Análise de sentimentos
- [ ] Multi-usuário
- [ ] Integração Google Analytics

### Q4 2025
- [ ] Aplicativo mobile
- [ ] White-label
- [ ] Marketplace de features
- [ ] Escalabilidade enterprise

---

**Última atualização:** Outubro 2025  
**Versão:** 1.0.0 (MVP)
