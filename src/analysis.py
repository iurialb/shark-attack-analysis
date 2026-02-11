"""
Script para análises exploratórias dos dados de ataques de tubarões
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_clean_data(filepath='data/attacks_clean.csv'):
    """Carrega os dados limpos"""
    df = pd.read_csv(filepath)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def basic_statistics(df):
    """Calcula estatísticas básicas"""
    print("=" * 60)
    print("ESTATÍSTICAS BÁSICAS")
    print("=" * 60)
    
    print(f"\nTotal de ataques registrados: {len(df):,}")
    
    if 'year' in df.columns:
        print(f"Período: {int(df['year'].min())} - {int(df['year'].max())}")
        print(f"Anos de dados: {int(df['year'].max() - df['year'].min())} anos")
    
    if 'is_fatal' in df.columns:
        total_fatal = df['is_fatal'].sum()
        total_known = df['is_fatal'].notna().sum()
        fatality_rate = (total_fatal / total_known) * 100 if total_known > 0 else 0
        print(f"\nTotal de ataques fatais: {int(total_fatal):,}")
        print(f"Taxa de fatalidade: {fatality_rate:.2f}%")
    
    if 'country' in df.columns:
        print(f"\nTotal de países: {df['country'].nunique()}")
    
    if 'species' in df.columns or 'species_' in df.columns:
        species_col = 'species' if 'species' in df.columns else 'species_'
        print(f"Espécies identificadas: {df[species_col].nunique()}")

def temporal_analysis(df):
    """Análise temporal dos ataques"""
    print("\n" + "=" * 60)
    print("ANÁLISE TEMPORAL")
    print("=" * 60)
    
    if 'year' in df.columns:
        # Ataques por década
        df['decade'] = (df['year'] // 10) * 10
        attacks_by_decade = df.groupby('decade').size().sort_index()
        
        print("\nAtaques por década:")
        for decade, count in attacks_by_decade.tail(10).items():
            print(f"  {int(decade)}s: {count:,} ataques")
        
        # Tendência recente
        recent_years = df[df['year'] >= 2000].groupby('year').size()
        if len(recent_years) > 0:
            avg_recent = recent_years.mean()
            print(f"\nMédia de ataques por ano (2000-presente): {avg_recent:.1f}")
    
    if 'month' in df.columns:
        attacks_by_month = df['month'].value_counts().sort_index()
        month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                       'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        print("\nAtaques por mês:")
        for month, count in attacks_by_month.items():
            if pd.notna(month) and 1 <= month <= 12:
                print(f"  {month_names[int(month)-1]}: {count:,} ataques")

def geographic_analysis(df):
    """Análise geográfica dos ataques"""
    print("\n" + "=" * 60)
    print("ANÁLISE GEOGRÁFICA")
    print("=" * 60)
    
    if 'country' in df.columns:
        top_countries = df['country'].value_counts().head(10)
        
        print("\nTop 10 países com mais ataques:")
        for i, (country, count) in enumerate(top_countries.items(), 1):
            percentage = (count / len(df)) * 100
            print(f"  {i}. {country}: {count:,} ataques ({percentage:.1f}%)")
    
    if 'area' in df.columns:
        print("\nTop 10 áreas/regiões:")
        top_areas = df['area'].value_counts().head(10)
        for i, (area, count) in enumerate(top_areas.items(), 1):
            print(f"  {i}. {area}: {count:,} ataques")

def species_analysis(df):
    """Análise por espécie de tubarão"""
    print("\n" + "=" * 60)
    print("ANÁLISE POR ESPÉCIE")
    print("=" * 60)
    
    species_col = None
    if 'species' in df.columns:
        species_col = 'species'
    elif 'species_' in df.columns:
        species_col = 'species_'
    
    if species_col:
        # Remover valores vazios e unknown
        species_data = df[df[species_col].notna() & (df[species_col] != '')]
        
        top_species = species_data[species_col].value_counts().head(10)
        
        print("\nTop 10 espécies mais envolvidas:")
        for i, (species, count) in enumerate(top_species.items(), 1):
            percentage = (count / len(species_data)) * 100
            print(f"  {i}. {species}: {count:,} ataques ({percentage:.1f}%)")
        
        # Fatalidade por espécie
        if 'is_fatal' in df.columns:
            print("\nTaxa de fatalidade por espécie (top 5):")
            for species in top_species.head(5).index:
                species_attacks = species_data[species_data[species_col] == species]
                fatal_attacks = species_attacks['is_fatal'].sum()
                total_attacks = species_attacks['is_fatal'].notna().sum()
                
                if total_attacks > 0:
                    fatality_rate = (fatal_attacks / total_attacks) * 100
                    print(f"  {species}: {fatality_rate:.1f}% ({int(fatal_attacks)}/{total_attacks})")

def activity_analysis(df):
    """Análise por atividade da vítima"""
    print("\n" + "=" * 60)
    print("ANÁLISE POR ATIVIDADE")
    print("=" * 60)
    
    if 'activity_category' in df.columns:
        activity_counts = df['activity_category'].value_counts()
        
        print("\nAtaques por tipo de atividade:")
        for activity, count in activity_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {activity}: {count:,} ataques ({percentage:.1f}%)")
        
        # Fatalidade por atividade
        if 'is_fatal' in df.columns:
            print("\nTaxa de fatalidade por atividade:")
            for activity in activity_counts.head(7).index:
                activity_attacks = df[df['activity_category'] == activity]
                fatal_attacks = activity_attacks['is_fatal'].sum()
                total_attacks = activity_attacks['is_fatal'].notna().sum()
                
                if total_attacks > 10:  # Apenas atividades com amostra significativa
                    fatality_rate = (fatal_attacks / total_attacks) * 100
                    print(f"  {activity}: {fatality_rate:.1f}% ({int(fatal_attacks)}/{total_attacks})")

def gender_analysis(df):
    """Análise por gênero"""
    if 'sex' in df.columns or 'gender' in df.columns:
        print("\n" + "=" * 60)
        print("ANÁLISE POR GÊNERO")
        print("=" * 60)
        
        gender_col = 'sex' if 'sex' in df.columns else 'gender'
        gender_counts = df[gender_col].value_counts()
        
        print("\nAtaques por gênero:")
        for gender, count in gender_counts.items():
            if pd.notna(gender):
                percentage = (count / len(df)) * 100
                print(f"  {gender}: {count:,} ataques ({percentage:.1f}%)")

def run_all_analyses(filepath='data/attacks_clean.csv'):
    """Executa todas as análises"""
    print("\n" + "=" * 80)
    print("ANÁLISE EXPLORATÓRIA DE ATAQUES DE TUBARÕES")
    print("=" * 80)
    
    df = load_clean_data(filepath)
    
    basic_statistics(df)
    temporal_analysis(df)
    geographic_analysis(df)
    species_analysis(df)
    activity_analysis(df)
    gender_analysis(df)
    
    print("\n" + "=" * 80)
    print("✅ Análise concluída!")
    print("=" * 80)
    
    return df

if __name__ == "__main__":
    df = run_all_analyses()
