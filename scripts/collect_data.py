#!/usr/bin/env python3
"""
Script para executar coleta de dados do Instagram
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapers import run_instagram_collection


def main():
    try:
        # Executar coleta
        results = run_instagram_collection()
        
        if results:
            print("\n✅ Coleta finalizada com sucesso!")
            print(f"📊 {len(results)} perfis atualizados")
        else:
            print("\n⚠️  Nenhum dado foi coletado")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Coleta interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro durante a coleta: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
