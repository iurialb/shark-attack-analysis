#!/usr/bin/env python3
"""
Script principal para executar toda a análise de ataques de tubarões
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_cleaning import clean_data
from analysis import run_all_analyses
from visualization import generate_all_visualizations

def main():
    """Executa o pipeline completo de análise"""
    print("\n" + "=" * 80)
    print("🦈 PIPELINE DE ANÁLISE DE ATAQUES DE TUBARÕES")
    print("=" * 80)
    
    # Verificar se os dados existem
    data_file = Path('data/attacks.csv')
    if not data_file.exists():
        print("\n❌ ERRO: Arquivo 'data/attacks.csv' não encontrado!")
        print("\nPor favor:")
        print("1. Acesse: https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset")
        print("2. Baixe o arquivo 'attacks.csv'")
        print("3. Coloque na pasta 'data/'")
        print("\nDepois execute este script novamente.")
        return
    
    try:
        # Etapa 1: Limpeza de dados
        print("\n" + "=" * 80)
        print("ETAPA 1/3: Limpeza de Dados")
        print("=" * 80)
        df_clean = clean_data()
        
        # Etapa 2: Análises
        print("\n" + "=" * 80)
        print("ETAPA 2/3: Análises Estatísticas")
        print("=" * 80)
        run_all_analyses()
        
        # Etapa 3: Visualizações
        print("\n" + "=" * 80)
        print("ETAPA 3/3: Geração de Visualizações")
        print("=" * 80)
        generate_all_visualizations()
        
        # Conclusão
        print("\n" + "=" * 80)
        print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        print("\nArquivos gerados:")
        print("  📊 Dados limpos: data/attacks_clean.csv")
        print("  📈 Gráficos: outputs/")
        print("\nPróximos passos:")
        print("  - Explore o notebook Jupyter: notebooks/exploratory_analysis.ipynb")
        print("  - Visualize os gráficos na pasta outputs/")
        print("  - Faça suas próprias análises!")
        
    except Exception as e:
        print(f"\n❌ ERRO durante a execução: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
