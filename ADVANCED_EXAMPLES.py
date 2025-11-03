"""
EXEMPLOS DE USO AVANÇADO
=========================

Este arquivo contém exemplos de como usar o sistema de forma programática
para análises customizadas, relatórios e automações.
"""

# ==================== Exemplo 1: Análise Customizada ====================

def exemplo_analise_customizada():
    """
    Como fazer análises customizadas dos dados
    """
    from database import db
    import pandas as pd
    
    # Pegar todos os dados dos últimos 30 dias
    df = db.get_instagram_dataframe(days=30)
    
    # Análise por perfil
    for username in df['username'].unique():
        df_user = df[df['username'] == username]
        
        print(f"\n📊 Análise de @{username}")
        print(f"   Total de coletas: {len(df_user)}")
        print(f"   Seguidores atuais: {df_user.iloc[-1]['followers']:,}")
        print(f"   Crescimento total: {df_user.iloc[-1]['followers'] - df_user.iloc[0]['followers']:+,}")
        
        # Média de crescimento diário
        days = (df_user.iloc[-1]['collected_at'] - df_user.iloc[0]['collected_at']).days
        if days > 0:
            avg_daily = (df_user.iloc[-1]['followers'] - df_user.iloc[0]['followers']) / days
            print(f"   Crescimento médio/dia: {avg_daily:+.1f}")


# ==================== Exemplo 2: Exportar Relatório ====================

def exemplo_exportar_relatorio():
    """
    Como exportar dados para análise externa
    """
    from database import db
    from datetime import datetime
    
    # Pegar dados
    df = db.get_instagram_dataframe(days=90)
    
    # Exportar CSV
    filename = f"relatorio_instagram_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Relatório exportado: {filename}")
    
    # Exportar Excel (requer openpyxl: pip install openpyxl)
    try:
        excel_filename = filename.replace('.csv', '.xlsx')
        df.to_excel(excel_filename, index=False, sheet_name='Instagram')
        print(f"✅ Relatório Excel exportado: {excel_filename}")
    except ImportError:
        print("⚠️  Para exportar Excel, instale: pip install openpyxl")


# ==================== Exemplo 3: Comparação de Perfis ====================

def exemplo_comparacao_perfis():
    """
    Comparar performance entre perfis
    """
    from database import db
    
    perfis = ['crismonteirosp', 'marinahelenabr', 'adriventurasp']
    
    print("\n" + "="*60)
    print("COMPARATIVO DE PERFIS - ÚLTIMOS 7 DIAS")
    print("="*60)
    
    rankings = []
    
    for username in perfis:
        growth = db.calculate_growth(username, days=7)
        
        if growth:
            rankings.append({
                'username': username,
                'crescimento': growth['growth'],
                'taxa': growth['growth_rate']
            })
            
            print(f"\n@{username}")
            print(f"  Seguidores: {growth['start_followers']:,} → {growth['end_followers']:,}")
            print(f"  Crescimento: {growth['growth']:+,} ({growth['growth_rate']:+.2f}%)")
    
    # Ranking por crescimento absoluto
    rankings.sort(key=lambda x: x['crescimento'], reverse=True)
    
    print("\n" + "="*60)
    print("🏆 RANKING POR CRESCIMENTO")
    print("="*60)
    
    for i, perfil in enumerate(rankings, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{emoji} {i}º lugar: @{perfil['username']} - {perfil['crescimento']:+,} seguidores")


# ==================== Exemplo 4: Alertas Customizados ====================

def exemplo_alertas():
    """
    Sistema de alertas para eventos importantes
    """
    from database import db
    
    perfil_principal = 'crismonteirosp'
    
    # Pegar crescimento recente
    growth = db.calculate_growth(perfil_principal, days=1)
    
    if not growth:
        print("⚠️  Dados insuficientes para análise")
        return
    
    print(f"\n🔔 ALERTAS PARA @{perfil_principal}")
    print("="*60)
    
    # Alerta: Crescimento excepcional
    if growth['growth'] > 1000:
        print("🎉 ALERTA POSITIVO: Crescimento excepcional!")
        print(f"   Ganhou {growth['growth']:,} seguidores em 1 dia!")
    
    # Alerta: Perda de seguidores
    elif growth['growth'] < -100:
        print("⚠️  ALERTA: Queda significativa de seguidores")
        print(f"   Perdeu {abs(growth['growth']):,} seguidores em 1 dia")
    
    # Alerta: Milestone alcançado
    current_followers = growth['end_followers']
    milestones = [10000, 25000, 50000, 100000, 250000, 500000, 1000000]
    
    for milestone in milestones:
        if growth['start_followers'] < milestone <= current_followers:
            print(f"🎊 MILESTONE: Alcançou {milestone:,} seguidores!")
    
    print("="*60)


# ==================== Exemplo 5: Previsão de Crescimento ====================

def exemplo_previsao():
    """
    Previsão simples de quando atingirá metas
    """
    from database import db
    from utils import estimate_time_to_goal
    
    perfil = 'crismonteirosp'
    meta = 100000  # Meta de seguidores
    
    # Calcular crescimento médio
    growth = db.calculate_growth(perfil, days=30)
    
    if not growth:
        print("⚠️  Dados insuficientes")
        return
    
    avg_daily_growth = growth['growth'] / 30
    current_followers = growth['end_followers']
    
    print(f"\n🎯 PREVISÃO PARA @{perfil}")
    print("="*60)
    print(f"Seguidores atuais: {current_followers:,}")
    print(f"Meta: {meta:,}")
    print(f"Crescimento médio/dia: {avg_daily_growth:+.1f}")
    
    # Estimar tempo para meta
    estimation = estimate_time_to_goal(current_followers, meta, avg_daily_growth)
    
    print(f"\n{estimation['message']}")
    if estimation['reachable'] and estimation['days'] > 0:
        print(f"Data estimada: {estimation['estimated_date']}")
    
    print("="*60)


# ==================== Exemplo 6: Análise de Engajamento ====================

def exemplo_analise_engajamento():
    """
    Análise detalhada de engajamento
    """
    from database import db
    
    df = db.get_instagram_dataframe(days=30)
    
    if df.empty or 'engagement_rate' not in df.columns:
        print("⚠️  Dados de engajamento não disponíveis")
        return
    
    print("\n💬 ANÁLISE DE ENGAJAMENTO")
    print("="*60)
    
    for username in df['username'].unique():
        df_user = df[df['username'] == username]
        
        # Filtrar apenas dados com engajamento
        df_eng = df_user[df_user['engagement_rate'].notna()]
        
        if df_eng.empty:
            continue
        
        avg_engagement = df_eng['engagement_rate'].mean()
        max_engagement = df_eng['engagement_rate'].max()
        min_engagement = df_eng['engagement_rate'].min()
        
        print(f"\n@{username}")
        print(f"  Taxa média: {avg_engagement:.2f}%")
        print(f"  Máxima: {max_engagement:.2f}%")
        print(f"  Mínima: {min_engagement:.2f}%")
        
        # Benchmark (taxa média Instagram: 1-3%)
        if avg_engagement > 3:
            print(f"  ✅ Engajamento EXCELENTE (acima da média)")
        elif avg_engagement > 1:
            print(f"  👍 Engajamento BOM (na média)")
        else:
            print(f"  ⚠️  Engajamento BAIXO (abaixo da média)")
    
    print("="*60)


# ==================== Exemplo 7: Automação com Schedule ====================

def exemplo_automacao_schedule():
    """
    Como automatizar coleta usando a biblioteca schedule
    Instale: pip install schedule
    """
    import schedule
    import time
    from scrapers import run_instagram_collection
    
    def job():
        print(f"\n🤖 Executando coleta automática...")
        run_instagram_collection()
    
    # Agendar coleta diária às 9h
    schedule.every().day.at("09:00").do(job)
    
    print("🤖 Bot de coleta automática iniciado!")
    print("📅 Coleta agendada para todo dia às 9h")
    print("Pressione Ctrl+C para parar\n")
    
    # Loop infinito
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto


# ==================== Como Usar ====================

if __name__ == "__main__":
    print("🎓 EXEMPLOS DE USO AVANÇADO")
    print("\nEscolha um exemplo para executar:")
    print("1. Análise Customizada")
    print("2. Exportar Relatório")
    print("3. Comparação de Perfis")
    print("4. Sistema de Alertas")
    print("5. Previsão de Crescimento")
    print("6. Análise de Engajamento")
    print("7. Automação com Schedule")
    
    try:
        opcao = input("\nOpção (1-7): ")
        
        exemplos = {
            '1': exemplo_analise_customizada,
            '2': exemplo_exportar_relatorio,
            '3': exemplo_comparacao_perfis,
            '4': exemplo_alertas,
            '5': exemplo_previsao,
            '6': exemplo_analise_engajamento,
            '7': exemplo_automacao_schedule,
        }
        
        if opcao in exemplos:
            exemplos[opcao]()
        else:
            print("❌ Opção inválida")
            
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!")
