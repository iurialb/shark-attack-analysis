"""
Script para criação de visualizações dos dados de ataques de tubarões
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configurações de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def ensure_output_dir():
    """Garante que o diretório de outputs existe"""
    Path('outputs').mkdir(exist_ok=True)

def load_data(filepath='data/attacks_clean.csv'):
    """Carrega os dados limpos"""
    df = pd.read_csv(filepath)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def plot_attacks_over_time(df):
    """Gráfico de ataques ao longo do tempo"""
    if 'year' not in df.columns:
        return
    
    ensure_output_dir()
    
    # Filtrar anos válidos e agrupar
    attacks_by_year = df[df['year'] >= 1900].groupby('year').size()
    
    plt.figure(figsize=(14, 6))
    plt.plot(attacks_by_year.index, attacks_by_year.values, linewidth=2, color='#0066cc')
    plt.fill_between(attacks_by_year.index, attacks_by_year.values, alpha=0.3, color='#0066cc')
    
    plt.title('Evolução dos Ataques de Tubarões ao Longo do Tempo', fontsize=16, fontweight='bold')
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Número de Ataques', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/attacks_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'attacks_over_time.png' criado")

def plot_top_countries(df):
    """Gráfico de países com mais ataques"""
    if 'country' not in df.columns:
        return
    
    ensure_output_dir()
    
    top_countries = df['country'].value_counts().head(15)
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top_countries)), top_countries.values, color='#e74c3c')
    plt.yticks(range(len(top_countries)), top_countries.index)
    plt.xlabel('Número de Ataques', fontsize=12)
    plt.title('Top 15 Países com Mais Ataques de Tubarões', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Adicionar valores nas barras
    for i, (idx, value) in enumerate(top_countries.items()):
        plt.text(value + 10, i, f'{value:,}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('outputs/top_countries.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'top_countries.png' criado")

def plot_attacks_by_month(df):
    """Gráfico de ataques por mês"""
    if 'month' not in df.columns:
        return
    
    ensure_output_dir()
    
    attacks_by_month = df['month'].value_counts().sort_index()
    month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(1, 13), [attacks_by_month.get(i, 0) for i in range(1, 13)], 
                   color='#3498db', edgecolor='black', linewidth=1.2)
    
    plt.xticks(range(1, 13), month_names)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('Número de Ataques', fontsize=12)
    plt.title('Distribuição de Ataques por Mês do Ano', fontsize=16, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('outputs/attacks_by_month.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'attacks_by_month.png' criado")

def plot_top_species(df):
    """Gráfico de espécies de tubarões"""
    species_col = 'species' if 'species' in df.columns else 'species_'
    
    if species_col not in df.columns:
        return
    
    ensure_output_dir()
    
    # Filtrar dados válidos
    species_data = df[df[species_col].notna() & (df[species_col] != '')]
    top_species = species_data[species_col].value_counts().head(10)
    
    plt.figure(figsize=(12, 8))
    colors = sns.color_palette("husl", len(top_species))
    bars = plt.barh(range(len(top_species)), top_species.values, color=colors)
    plt.yticks(range(len(top_species)), top_species.index)
    plt.xlabel('Número de Ataques', fontsize=12)
    plt.title('Top 10 Espécies de Tubarões Envolvidas em Ataques', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Adicionar valores
    for i, (idx, value) in enumerate(top_species.items()):
        plt.text(value + 5, i, f'{value:,}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('outputs/top_species.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'top_species.png' criado")

def plot_activity_categories(df):
    """Gráfico de ataques por atividade"""
    if 'activity_category' not in df.columns:
        return
    
    ensure_output_dir()
    
    activity_counts = df['activity_category'].value_counts()
    
    # Gráfico de pizza
    plt.figure(figsize=(10, 10))
    colors = sns.color_palette("Set3", len(activity_counts))
    
    wedges, texts, autotexts = plt.pie(activity_counts.values, 
                                        labels=activity_counts.index,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 11})
    
    plt.title('Distribuição de Ataques por Tipo de Atividade', fontsize=16, fontweight='bold', pad=20)
    
    # Melhorar legibilidade
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig('outputs/activity_categories.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'activity_categories.png' criado")

def plot_fatality_rate(df):
    """Gráfico de taxa de fatalidade"""
    if 'is_fatal' not in df.columns:
        return
    
    ensure_output_dir()
    
    fatal_counts = df['is_fatal'].value_counts()
    labels = ['Não Fatal', 'Fatal']
    values = [fatal_counts.get(0, 0), fatal_counts.get(1, 0)]
    
    plt.figure(figsize=(8, 8))
    colors = ['#2ecc71', '#e74c3c']
    
    wedges, texts, autotexts = plt.pie(values, 
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        explode=(0.05, 0.05),
                                        textprops={'fontsize': 13, 'fontweight': 'bold'})
    
    plt.title('Taxa de Fatalidade dos Ataques', fontsize=16, fontweight='bold', pad=20)
    
    for autotext in autotexts:
        autotext.set_color('white')
    
    plt.tight_layout()
    plt.savefig('outputs/fatality_rate.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'fatality_rate.png' criado")

def plot_decade_comparison(df):
    """Gráfico comparando décadas"""
    if 'year' not in df.columns:
        return
    
    ensure_output_dir()
    
    df['decade'] = (df['year'] // 10) * 10
    attacks_by_decade = df[df['decade'] >= 1900].groupby('decade').size()
    
    plt.figure(figsize=(14, 6))
    bars = plt.bar(attacks_by_decade.index, attacks_by_decade.values, 
                   width=8, color='#9b59b6', edgecolor='black', linewidth=1.2)
    
    plt.xlabel('Década', fontsize=12)
    plt.ylabel('Número de Ataques', fontsize=12)
    plt.title('Comparação de Ataques por Década', fontsize=16, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    # Adicionar valores
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('outputs/decade_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 'decade_comparison.png' criado")

def create_interactive_map(df):
    """Cria mapa interativo de ataques (se houver coordenadas)"""
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return
    
    ensure_output_dir()
    
    # Filtrar coordenadas válidas
    map_data = df[df['latitude'].notna() & df['longitude'].notna()].copy()
    
    if len(map_data) == 0:
        return
    
    # Criar mapa interativo
    fig = px.scatter_mapbox(map_data.head(1000),  # Limitar para performance
                            lat='latitude',
                            lon='longitude',
                            hover_name='country' if 'country' in df.columns else None,
                            hover_data=['year'] if 'year' in df.columns else None,
                            color='is_fatal' if 'is_fatal' in df.columns else None,
                            zoom=1,
                            height=600)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    fig.write_html('outputs/interactive_map.html')
    print("✓ Mapa interativo 'interactive_map.html' criado")

def generate_all_visualizations(filepath='data/attacks_clean.csv'):
    """Gera todas as visualizações"""
    print("\n" + "=" * 60)
    print("GERANDO VISUALIZAÇÕES")
    print("=" * 60 + "\n")
    
    df = load_data(filepath)
    
    plot_attacks_over_time(df)
    plot_top_countries(df)
    plot_attacks_by_month(df)
    plot_top_species(df)
    plot_activity_categories(df)
    plot_fatality_rate(df)
    plot_decade_comparison(df)
    create_interactive_map(df)
    
    print("\n" + "=" * 60)
    print("✅ Todas as visualizações foram criadas na pasta 'outputs/'")
    print("=" * 60)

if __name__ == "__main__":
    generate_all_visualizations()
