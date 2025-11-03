#!/usr/bin/env python3
"""
Script para iniciar o dashboard
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard import run_server


def main():
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard encerrado. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao iniciar dashboard: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
