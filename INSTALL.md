# 🚀 Guia de Instalação Rápida

> **Tempo estimado:** 15-20 minutos  
> **Nível:** Iniciante  
> **Sistema:** Mac OS X

---

## 📋 O que você vai precisar

- ✅ Mac OS X 10.14 ou superior
- ✅ Conexão com internet
- ✅ Conta no Apify (gratuita - vamos criar juntos)
- ✅ 20 minutos de tempo

---

## 🎯 Passo a Passo

### 1️⃣ Instalar Python

**Verificar se já tem Python:**
```bash
python3 --version
```

Se aparecer `Python 3.9.x` ou superior, **você já tem!** ✅  
Pule para o passo 2.

**Se não tiver, instale via Homebrew:**

```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python
```

---

### 2️⃣ Baixar o Projeto

```bash
# Navegue até onde quer salvar
cd ~/Documents

# (O projeto já está aqui, só navegue até ele)
cd social-monitor
```

---

### 3️⃣ Instalar Dependências

```bash
# Instale todas as bibliotecas necessárias
pip3 install -r requirements.txt
```

**Vai instalar:**
- Apify Client (coleta de dados)
- Plotly Dash (dashboard)
- SQLAlchemy (banco de dados)
- Pandas (análise de dados)
- E mais algumas...

⏱️ **Tempo:** ~3 minutos

---

### 4️⃣ Criar Conta Apify (GRÁTIS!)

1. **Acesse:** https://apify.com/sign-up

2. **Crie sua conta** (use Google/GitHub para facilitar)

3. **Você ganha $5 grátis!** 🎉
   - Suficiente para ~10.000 páginas de scraping
   - Aproximadamente 1 mês de uso do nosso sistema

4. **Pegue seu token:**
   - Clique no seu avatar (canto superior direito)
   - `Settings` → `Integrations`
   - Copie o **"Personal API Token"**
   - Vai começar com `apify_api_...`

![Apify Token](https://i.imgur.com/placeholder.png)

---

### 5️⃣ Configurar o Projeto

```bash
# Criar arquivo de configuração
cp .env.example .env

# Abrir no editor de texto
nano .env
# Ou use TextEdit, VSCode, etc
```

**Cole seu token Apify:**
```bash
APIFY_API_TOKEN=apify_api_seu_token_aqui_colado
```

**Salvar:**
- No nano: `Ctrl+O`, `Enter`, `Ctrl+X`
- No TextEdit: `Cmd+S`

---

### 6️⃣ Criar Banco de Dados

```bash
python3 scripts/setup_database.py
```

**Você verá:**
```
🗄️  CONFIGURANDO BANCO DE DADOS
============================================================
📁 Criando banco em: data/social_monitor.db
✅ Banco de dados configurado com sucesso!

📋 Tabelas criadas:
   • instagram_profiles
   • collection_logs
   • daily_metrics
```

---

### 7️⃣ Coletar Dados do Instagram! 🎯

```bash
python3 scripts/collect_data.py
```

**O que vai acontecer:**
1. Conecta com Apify ✅
2. Busca dados de cada perfil:
   - @crismonteirosp
   - @marinahelenabr
   - @adriventurasp
   - @leosiqueirabr
3. Salva tudo no banco de dados ✅

⏱️ **Tempo:** ~2-3 minutos  
💰 **Custo:** ~$0.40 (seus créditos grátis cobrem!)

---

### 8️⃣ Abrir o Dashboard! 🎨

```bash
python3 scripts/run_dashboard.py
```

**Abra seu navegador em:**
```
http://localhost:8050
```

---

## 🎉 PRONTO!

Você verá um dashboard profissional com:

- 📈 **Gráfico de crescimento** ao longo do tempo
- 📊 **Taxa de crescimento** (últimos 7 dias)
- 💬 **Comparativo de engajamento**
- 📋 **Tabela com todas as métricas**

---

## 🔥 Próximos Passos

### Coleta Automática Diária

**Opção 1: Manual**
```bash
# Execute todo dia no mesmo horário
python3 scripts/collect_data.py
```

**Opção 2: Automática (Cron)**
```bash
# Abrir editor cron
crontab -e

# Adicionar (coleta todo dia às 9h)
0 9 * * * cd /Users/seu-usuario/Documents/social-monitor && python3 scripts/collect_data.py
```

---

## 📚 Documentação

- **README.md** - Visão geral completa
- **QUICKSTART.py** - Guia detalhado de início
- **ARCHITECTURE.md** - Como o sistema funciona
- **TROUBLESHOOTING.py** - Soluções para problemas
- **ADVANCED_EXAMPLES.py** - Exemplos avançados
- **CHECKLIST.py** - Verificar se tudo está OK

---

## 🆘 Problemas?

### "pip3: command not found"
```bash
# Instalar Python novamente
brew install python
```

### "Token inválido"
- Verifique se copiou o token completo
- Deve começar com `apify_api_`
- Sem espaços extras

### "Port 8050 already in use"
```bash
# Matar processo anterior
kill -9 $(lsof -ti:8050)
```

### Outros problemas
Consulte **TROUBLESHOOTING.py** para soluções detalhadas!

---

## 💰 Custos

**Fase Atual (MVP):**
- Apify Free Tier: **$0/mês** (primeiros $5 grátis)
- Hospedagem: **$0/mês** (roda no seu Mac)
- **Total: GRÁTIS para testar!** 🎉

**Uso Regular:**
- 4 perfis, 1x por dia = ~$12/mês de consumo
- Apify Starter: $49/mês (recomendado)

---

## 🎯 Checklist Rápido

```
[ ] Python instalado
[ ] Dependências instaladas
[ ] Conta Apify criada
[ ] Token configurado no .env
[ ] Banco de dados criado
[ ] Primeira coleta realizada
[ ] Dashboard funcionando
```

**Todos marcados?** Parabéns! 🎊

---

## 📞 Suporte

- **Documentação Apify:** https://docs.apify.com
- **Plotly Dash:** https://dash.plotly.com
- **Troubleshooting:** Veja arquivo `TROUBLESHOOTING.py`

---

**Desenvolvido com ❤️ para @crismonteirosp**

**Versão:** 1.0.0 MVP  
**Data:** Outubro 2025
