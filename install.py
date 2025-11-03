#!/usr/bin/env python3
"""
🚀 INSTALADOR AUTOMÁTICO - SOCIAL MEDIA MONITOR
===============================================

Este script facilita a instalação e configuração inicial do sistema.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    """Imprime banner bonito"""
    print("\n" + "="*60)
    print("🚀 INSTALADOR AUTOMÁTICO")
    print("   Social Media Monitor v1.0")
    print("="*60 + "\n")


def check_python():
    """Verifica versão do Python"""
    print("🔍 Verificando Python...")
    
    version = sys.version_info
    if version >= (3, 9):
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} detectado")
        print("   ⚠️  Necessário Python 3.9 ou superior")
        print("\n   Instale via: brew install python")
        return False


def install_dependencies():
    """Instala dependências do requirements.txt"""
    print("\n📦 Instalando dependências...")
    
    if not Path("requirements.txt").exists():
        print("   ❌ requirements.txt não encontrado!")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print("   ✅ Todas as dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print("   ❌ Erro ao instalar dependências")
        print(f"   {e.stderr.decode()[:200]}")
        return False


def setup_env():
    """Configura arquivo .env"""
    print("\n⚙️  Configurando arquivo .env...")
    
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if env_path.exists():
        print("   ⚠️  Arquivo .env já existe")
        response = input("   Deseja sobrescrever? (s/N): ")
        if response.lower() != 's':
            print("   ⏭️  Mantendo .env existente")
            return True
    
    if not example_path.exists():
        print("   ❌ .env.example não encontrado!")
        return False
    
    # Copiar template
    with open(example_path, 'r') as f:
        content = f.read()
    
    # Pedir token
    print("\n   🔑 Configure seu token Apify:")
    print("   1. Acesse: https://apify.com/sign-up")
    print("   2. Crie conta gratuita (use Google/GitHub)")
    print("   3. Settings → Integrations → copie o token")
    print()
    
    token = input("   Cole seu token Apify: ").strip()
    
    if not token:
        print("   ⚠️  Token vazio, usando template padrão")
        with open(env_path, 'w') as f:
            f.write(content)
    else:
        # Validar token
        if not token.startswith("apify_api_"):
            print("   ⚠️  Token parece inválido (deve começar com 'apify_api_')")
            print("   Mas vou salvar mesmo assim...")
        
        content = content.replace("your_apify_token_here", token)
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("   ✅ Token configurado!")
    
    return True


def setup_database():
    """Configura banco de dados"""
    print("\n🗄️  Configurando banco de dados...")
    
    try:
        # Importar depois de instalar dependências
        sys.path.insert(0, str(Path(__file__).parent))
        from database import db
        
        db.create_tables()
        print("   ✅ Banco de dados criado")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar banco: {str(e)[:100]}")
        return False


def run_first_collection():
    """Pergunta se quer executar primeira coleta"""
    print("\n📊 Primeira coleta de dados")
    print("   Isso vai buscar dados dos perfis configurados do Instagram")
    print("   Custo estimado: ~$0.40 em créditos Apify")
    print()
    
    response = input("   Executar primeira coleta agora? (S/n): ")
    
    if response.lower() == 'n':
        print("   ⏭️  Você pode executar depois com:")
        print("      python3 scripts/collect_data.py")
        return True
    
    try:
        from scrapers import run_instagram_collection
        
        print("\n   🔄 Coletando dados...")
        results = run_instagram_collection()
        
        if results:
            print(f"   ✅ {len(results)} perfis coletados!")
            return True
        else:
            print("   ⚠️  Nenhum dado coletado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro na coleta: {str(e)[:100]}")
        print("   Tente executar manualmente depois:")
        print("      python3 scripts/collect_data.py")
        return False


def print_next_steps():
    """Imprime próximos passos"""
    print("\n" + "="*60)
    print("🎉 INSTALAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n🎯 Próximos Passos:\n")
    print("1️⃣  Iniciar o dashboard:")
    print("   python3 scripts/run_dashboard.py")
    print()
    print("2️⃣  Abrir no navegador:")
    print("   http://localhost:8050")
    print()
    print("3️⃣  Coletar dados diariamente:")
    print("   python3 scripts/collect_data.py")
    print()
    print("📚 Documentação:")
    print("   • README.md - Visão geral")
    print("   • QUICKSTART.py - Guia detalhado")
    print("   • TROUBLESHOOTING.py - Problemas comuns")
    print()
    print("💡 Dica: Execute o checklist para verificar tudo:")
    print("   python3 CHECKLIST.py --verify")
    print("\n" + "="*60 + "\n")


def main():
    """Função principal do instalador"""
    print_banner()
    
    # Checklist de instalação
    steps = [
        ("Verificar Python", check_python),
        ("Instalar dependências", install_dependencies),
        ("Configurar .env", setup_env),
        ("Criar banco de dados", setup_database),
        ("Primeira coleta (opcional)", run_first_collection),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        if not step_func():
            failed_steps.append(step_name)
            
            if step_name != "Primeira coleta (opcional)":
                print(f"\n❌ Instalação falhou em: {step_name}")
                print("Consulte TROUBLESHOOTING.py para ajuda")
                sys.exit(1)
    
    # Sucesso!
    print_next_steps()
    
    # Perguntar se quer iniciar dashboard
    print("Deseja iniciar o dashboard agora? (S/n): ", end="")
    response = input().strip()
    
    if response.lower() != 'n':
        print("\n🚀 Iniciando dashboard...\n")
        try:
            subprocess.run([sys.executable, "scripts/run_dashboard.py"])
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard encerrado. Até logo!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        print("Consulte TROUBLESHOOTING.py ou tente instalação manual")
        sys.exit(1)
