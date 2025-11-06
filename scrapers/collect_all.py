"""
🎯 Script completo de coleta
Coleta dados do Notion E Instagram
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("\n" + "="*70)
print("🚀 COLETA COMPLETA - RADAR DAS REDES")
print("="*70 + "\n")

# 1. Coleta do Notion
print("📊 FASE 1: Coletando dados do Notion...")
print("-" * 70)
os.system('python3 scrapers/notion_scraper.py')

print("\n")

# 2. Coleta do Instagram
print("📸 FASE 2: Coletando dados do Instagram...")
print("-" * 70)
os.system('python3 scrapers/instagram_scraper.py')

print("\n" + "="*70)
print("✅ COLETA FINALIZADA!")
print("="*70 + "\n")
