# Análise de Ataques de Tubarões

Análise exploratória de dados sobre ataques de tubarões ao redor do mundo usando Python.

## Sobre o Projeto

Este projeto realiza uma análise exploratória completa da base de dados **Global Shark Attack File**, que contém informações detalhadas sobre milhares de ataques de tubarões registrados globalmente.

## Objetivos

- Explorar padrões geográficos e temporais dos ataques de tubarões
- Identificar as espécies de tubarões mais envolvidas nos ataques
- Analisar a relação entre atividades humanas e ataques
- Visualizar tendências e estatísticas relevantes

## Estrutura do Projeto

```
shark-attack-analysis/
│
├── data/                   # Dados (não versionados)
│   └── attacks.csv
├── notebooks/              # Jupyter notebooks com análises
│   └── exploratory_analysis.ipynb
├── src/                    # Scripts Python
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualization.py
├── outputs/                # Gráficos e resultados
├── requirements.txt        # Dependências
└── README.md
```

## Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/iurialb/shark-attack-analysis.git
cd shark-attack-analysis
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Baixe os dados

Faça o download do dataset do Kaggle:
- Acesse: https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset
- Baixe o arquivo `attacks.csv`
- Coloque na pasta `data/`

**Nota:** Você precisará de uma conta no Kaggle (gratuita)

### 4. Execute a análise

```bash
# Limpar os dados
python src/data_cleaning.py

# Executar análises
python src/analysis.py

# Ou abra o notebook Jupyter
jupyter notebook notebooks/exploratory_analysis.ipynb
```

## Principais Análises

- **Distribuição Geográfica**: Mapa de calor dos ataques por país e região
- **Tendências Temporais**: Evolução dos ataques ao longo das décadas
- **Espécies**: Ranking das espécies mais envolvidas em ataques
- **Atividades**: Relação entre atividade da vítima e tipo de ataque
- **Fatalidade**: Taxa de fatalidade por região e espécie
- **Sazonalidade**: Padrões mensais e sazonais

##  Tecnologias Utilizadas

- **Python 3.8+**
- **Pandas**: Manipulação e análise de dados
- **Matplotlib & Seaborn**: Visualizações
- **Plotly**: Gráficos interativos
- **Jupyter Notebook**: Ambiente de análise

## Exemplos de Visualizações

Os gráficos gerados incluem:
- Mapas de calor geográficos
- Séries temporais
- Gráficos de barras e pizza
- Box plots e histogramas

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas análises
- Melhorar visualizações
- Adicionar features

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Fonte dos Dados

Os dados utilizados neste projeto vêm do **Global Shark Attack File**, disponível no Kaggle:
- Dataset: [Shark Attack Dataset](https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset)
