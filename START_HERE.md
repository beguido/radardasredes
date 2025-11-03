# 👋 COMECE AQUI!

> **Bem-vindo ao Social Media Monitor!**  
> Sistema profissional de monitoramento de Instagram com dashboards interativos.

---

## 🎯 O que este sistema faz?

✨ **Coleta automaticamente** dados do Instagram  
📊 **Exibe dashboards profissionais** com gráficos interativos  
📈 **Acompanha crescimento** e engajamento ao longo do tempo  
⚡ **Compara perfis** e identifica tendências  

**Perfis monitorados:**
- 🎯 @crismonteirosp (principal)
- 📊 @marinahelenabr
- 📊 @adriventurasp
- 📊 @leosiqueirabr

---

## 🚀 Instalação Rápida (15 minutos)

### Opção 1: Instalação Automática (Recomendada)

```bash
# Abra o Terminal e execute:
python3 install.py
```

O instalador vai:
1. ✅ Verificar Python
2. ✅ Instalar dependências
3. ✅ Configurar seu token Apify
4. ✅ Criar banco de dados
5. ✅ Coletar primeiros dados
6. ✅ Abrir dashboard automaticamente!

### Opção 2: Instalação Manual

Siga o guia detalhado: **[INSTALL.md](INSTALL.md)**

---

## 📖 Guia Completo

Após instalar, você terá acesso a:

### 🎨 Dashboard Interativo

```bash
# Iniciar dashboard
python3 scripts/run_dashboard.py

# Abrir navegador em:
http://localhost:8050
```

**Recursos do Dashboard:**
- 📈 Timeline de crescimento de seguidores
- 📊 Taxa de crescimento (%)
- 💬 Análise de engajamento
- 📋 Tabela comparativa
- 🔄 Coleta de dados com um clique

### 📊 Coletar Novos Dados

```bash
# Coleta manual (execute diariamente)
python3 scripts/collect_data.py
```

---

## 📚 Documentação Completa

| Arquivo | Descrição |
|---------|-----------|
| **[INSTALL.md](INSTALL.md)** | 📘 Guia de instalação passo a passo |
| **[README.md](README.md)** | 📗 Documentação completa do projeto |
| **[QUICKSTART.py](QUICKSTART.py)** | 🚀 Guia rápido de início |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ Como o sistema funciona |
| **[TROUBLESHOOTING.py](TROUBLESHOOTING.py)** | 🔧 Soluções para problemas |
| **[ADVANCED_EXAMPLES.py](ADVANCED_EXAMPLES.py)** | 💡 Exemplos avançados de uso |
| **[CHECKLIST.py](CHECKLIST.py)** | ✅ Verificar se tudo está OK |

---

## 💰 Custos

### Fase Atual (MVP)
- **Apify Free Tier:** $0/mês ($5 grátis para começar!)
- **Hospedagem:** $0/mês (roda no seu Mac)
- **Total: GRÁTIS!** 🎉

### Uso Regular
- 4 perfis, 1x/dia ≈ $12/mês consumo
- Apify Starter: $49/mês (recomendado)

---

## 🆘 Problemas?

### Erros Comuns

**"pip3: command not found"**
```bash
brew install python
```

**"Token inválido"**
- Verifique se copiou o token completo do Apify
- Deve começar com `apify_api_`

**"Port 8050 already in use"**
```bash
kill -9 $(lsof -ti:8050)
```

**Outros problemas?**  
👉 Veja **[TROUBLESHOOTING.py](TROUBLESHOOTING.py)** com soluções completas!

---

## ⚡ Comandos Rápidos

```bash
# Instalar tudo
python3 install.py

# Verificar instalação
python3 CHECKLIST.py --verify

# Configurar banco
python3 scripts/setup_database.py

# Coletar dados
python3 scripts/collect_data.py

# Iniciar dashboard
python3 scripts/run_dashboard.py

# Ver exemplos avançados
python3 ADVANCED_EXAMPLES.py
```

---

## 🎓 Próximos Passos

Depois de instalar e explorar:

1. **Configure coleta automática**
   - Veja seção "Automação" no README.md
   - Use cron para coletas diárias

2. **Explore análises avançadas**
   - Execute ADVANCED_EXAMPLES.py
   - Crie seus próprios scripts de análise

3. **Planeje expansão**
   - Adicione YouTube, TikTok
   - Deploy em servidor
   - Automatize relatórios

---

## 📞 Suporte e Recursos

- **Documentação Apify:** https://docs.apify.com
- **Plotly Dash:** https://dash.plotly.com
- **Stack Overflow:** Procure por "plotly dash" ou "apify python"

---

## 🎉 Pronto para Começar?

```bash
# Execute o instalador agora:
python3 install.py
```

**Em 15 minutos você terá um dashboard profissional funcionando!**

---

**Desenvolvido com ❤️ para @crismonteirosp**

*Versão 1.0.0 - MVP*  
*Outubro 2025*
