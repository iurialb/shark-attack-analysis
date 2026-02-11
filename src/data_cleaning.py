"""
Script para limpeza e pré-processamento dos dados de ataques de tubarões
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_data(filepath='data/attacks.csv'):
    """Carrega os dados brutos"""
    print(f"Carregando dados de {filepath}...")
    df = pd.read_csv(filepath, encoding='latin-1', low_memory=False)
    print(f"Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df

def clean_column_names(df):
    """Padroniza nomes das colunas"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def clean_dates(df):
    """Limpa e converte datas"""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
    elif 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
    
    return df

def clean_species(df):
    """Limpa dados de espécies de tubarões"""
    if 'species' in df.columns or 'species_' in df.columns:
        species_col = 'species' if 'species' in df.columns else 'species_'
        
        # Remove espaços extras
        df[species_col] = df[species_col].str.strip()
        
        # Padroniza valores comuns
        species_mapping = {
            'white shark': 'White shark',
            'bull shark': 'Bull shark',
            'tiger shark': 'Tiger shark',
            'blue shark': 'Blue shark',
            'blacktip shark': 'Blacktip shark',
            'great white': 'White shark',
            'great white shark': 'White shark',
        }
        
        df[species_col] = df[species_col].str.lower().replace(species_mapping)
    
    return df

def clean_country(df):
    """Limpa dados de países"""
    if 'country' in df.columns:
        df['country'] = df['country'].str.strip()
        
        # Padroniza nomes de países
        country_mapping = {
            'usa': 'USA',
            'united states': 'USA',
            'united states of america': 'USA',
            'australia ': 'AUSTRALIA',
            'south africa': 'SOUTH AFRICA',
        }
        
        df['country'] = df['country'].str.upper().replace(country_mapping)
    
    return df

def clean_activity(df):
    """Limpa dados de atividade da vítima"""
    if 'activity' in df.columns:
        df['activity'] = df['activity'].str.strip().str.title()
        
        # Categoriza atividades principais
        df['activity_category'] = df['activity'].str.lower().apply(categorize_activity)
    
    return df

def categorize_activity(activity):
    """Categoriza atividades em grupos principais"""
    if pd.isna(activity):
        return 'Unknown'
    
    activity = activity.lower()
    
    if any(word in activity for word in ['surf', 'surfing', 'board']):
        return 'Surfing'
    elif any(word in activity for word in ['swim', 'swimming', 'bathing']):
        return 'Swimming'
    elif any(word in activity for word in ['dive', 'diving', 'snorkel']):
        return 'Diving'
    elif any(word in activity for word in ['fish', 'fishing']):
        return 'Fishing'
    elif any(word in activity for word in ['spear', 'spearfishing']):
        return 'Spearfishing'
    elif any(word in activity for word in ['kayak', 'canoe', 'boat']):
        return 'Boating'
    else:
        return 'Other'

def clean_fatal(df):
    """Limpa dados de fatalidade"""
    if 'fatal_(y/n)' in df.columns:
        df['fatal'] = df['fatal_(y/n)'].str.strip().str.upper()
        df['is_fatal'] = df['fatal'].apply(lambda x: 1 if x == 'Y' else (0 if x == 'N' else np.nan))
    elif 'fatal' in df.columns:
        df['is_fatal'] = df['fatal'].str.strip().str.upper().apply(lambda x: 1 if x == 'Y' else (0 if x == 'N' else np.nan))
    
    return df

def remove_duplicates(df):
    """Remove duplicatas"""
    initial_count = len(df)
    df = df.drop_duplicates()
    removed = initial_count - len(df)
    if removed > 0:
        print(f"Removidas {removed} linhas duplicadas")
    return df

def filter_valid_years(df, min_year=1900, max_year=2025):
    """Filtra anos válidos"""
    if 'year' in df.columns:
        initial_count = len(df)
        df = df[(df['year'] >= min_year) & (df['year'] <= max_year)]
        removed = initial_count - len(df)
        if removed > 0:
            print(f"Removidas {removed} linhas com anos inválidos")
    return df

def clean_data(input_file='data/attacks.csv', output_file='data/attacks_clean.csv'):
    """Pipeline completo de limpeza de dados"""
    print("=" * 60)
    print("Iniciando limpeza de dados...")
    print("=" * 60)
    
    # Carregar dados
    df = load_data(input_file)
    
    # Aplicar limpezas
    df = clean_column_names(df)
    df = clean_dates(df)
    df = clean_species(df)
    df = clean_country(df)
    df = clean_activity(df)
    df = clean_fatal(df)
    df = remove_duplicates(df)
    df = filter_valid_years(df)
    
    # Salvar dados limpos
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_file, index=False)
    print(f"\nDados limpos salvos em: {output_file}")
    print(f"Total de registros: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")
    
    # Mostrar informações básicas
    print("\n" + "=" * 60)
    print("Informações dos dados limpos:")
    print("=" * 60)
    print(df.info())
    
    return df

if __name__ == "__main__":
    df_clean = clean_data()
    print("\n✅ Limpeza concluída com sucesso!")
