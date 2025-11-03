#!/usr/bin/env python3
"""
Script para setup inicial do banco de dados
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import db
from config import settings


def main():
    print("\n" + "="*60)
    print("🗄️  CONFIGURANDO BANCO DE DADOS")
    print("="*60)
    
    print(f"\n📁 Criando banco em: {settings.DATABASE_PATH}")
    
    try:
        # Criar tabelas
        db.create_tables()
        
        print("\n✅ Banco de dados configurado com sucesso!")
        print("\n📋 Tabelas criadas:")
        print("   • instagram_profiles")
        print("   • collection_logs")
        print("   • daily_metrics")
        
        print("\n🎯 Próximos passos:")
        print("   1. Configure seu token Apify no arquivo .env")
        print("   2. Execute: python3 scripts/collect_data.py")
        print("   3. Inicie o dashboard: python3 scripts/run_dashboard.py")
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erro ao configurar banco: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
