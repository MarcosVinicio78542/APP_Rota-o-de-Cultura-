import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados dos arquivos Excel
rendimento_long = pd.read_excel('rendimento_long.xlsx', sheet_name=None)
rendimento_short = pd.read_excel('rendimento_short.xlsx', sheet_name=None)
tabela = pd.read_csv('tabela.csv')

# Extrair os DataFrames para cada cultura
soja_long = rendimento_long['soja_long']
soja_short = rendimento_short['soja_short']
arroz_long = rendimento_long['arroz_long']
arroz_short = rendimento_short['arroz_short']
feijao_long = rendimento_long['feijao_long']
feijao_short = rendimento_short['feijao_short']

# Selecionar município
municipios_unicos = tabela['Municipio'].unique()
municipio_selecionado = st.selectbox('Selecione o município', municipios_unicos)

datas_fixas = ["01-09", "11-09", "21-09", "01-10", "11-10", "21-10", "01-11", "11-11", "21-11"]

def plotar_graficos(df_short, df_long, cultura):
    """Gera boxplots e gráficos de violino para uma cultura específica"""
    # Filtrando os índices do município selecionado
    p = np.where(tabela['Municipio'] == municipio_selecionado)[0]
    
    df_short_filtrado = df_short.iloc[p]
    df_short_filtrado = df_short_filtrado.T
    df_short_filtrado.columns = datas_fixas  # Ajustando os nomes das colunas

    df_long_filtrado = df_long.iloc[p]
    df_long_filtrado = df_long_filtrado.T
    df_long_filtrado.columns = datas_fixas

    st.write(f"## Gráficos de Rendimento para {cultura} - Município {municipio_selecionado}")

    # Criando os gráficos lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Boxplot - Ciclo Short
    sns.boxplot(data=df_short_filtrado, ax=axes[0])
    axes[0].set_title(f'Boxplot {cultura} - Ciclo Short')
    axes[0].set_xlabel("Data de Plantio")
    axes[0].set_ylabel("Rendimento (kg/ha)")

    # Boxplot - Ciclo Long
    sns.boxplot(data=df_long_filtrado, ax=axes[1])
    axes[1].set_title(f'Boxplot {cultura} - Ciclo Long')
    axes[1].set_xlabel("Data de Plantio")
    axes[1].set_ylabel("Rendimento (kg/ha)")

    st.pyplot(fig)

    # Criando os gráficos de violino lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico de violino - Ciclo Short
    sns.violinplot(data=df_short_filtrado, ax=axes[0])
    axes[0].set_title(f'Gráfico de Violino {cultura} - Ciclo Short')
    axes[0].set_xlabel("Data de Plantio")
    axes[0].set_ylabel("Rendimento (kg/ha)")

    # Gráfico de violino - Ciclo Long
    sns.violinplot(data=df_long_filtrado, ax=axes[1])
    axes[1].set_title(f'Gráfico de Violino {cultura} - Ciclo Long')
    axes[1].set_xlabel("Data de Plantio")
    axes[1].set_ylabel("Rendimento (kg/ha)")

    st.pyplot(fig)

# Gerando gráficos para cada cultura
plotar_graficos(soja_short, soja_long, 'Soja')
plotar_graficos(arroz_short, arroz_long, 'Arroz')
plotar_graficos(feijao_short, feijao_long, 'Feijão')
