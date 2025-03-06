import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Lendo o arquivo com a tabela já pronta
tabela = pd.read_csv('C:/Users/jacim/Downloads/tabela.csv').iloc[:, 1:]

# Lendo os arquivos das tabelas de longo e curto prazo para o método do cotovelo
tabela_long = pd.read_csv('C:/Users/jacim/Downloads/tabela-long.csv')
tabela_long = tabela_long.drop(columns=tabela_long.columns[0])  # Remover a primeira coluna (se necessário)

# Verificando os nomes das colunas de tabela_long
print(tabela_long.columns)  # Verifique se 'MP_Long' está presente aqui

# Caso a coluna 'MP_Long' não esteja correta, substitua pelo nome correto
# Ajuste conforme a saída do print(tabela_long.columns)
tabela_long = tabela_long.rename(columns={'MP_Long': 'MP_Long'})  # Renomeie se necessário

tabela_short = pd.read_csv('C:/Users/jacim/Downloads/tabela-short.csv')
tabela_short = tabela_short.drop(columns=tabela_short.columns[0])  # Remover a primeira coluna (se necessário)


# Caso a coluna 'MP_Short' não esteja correta, substitua pelo nome correto
# Ajuste conforme a saída do print(tabela_short.columns)
tabela_short = tabela_short.rename(columns={'MP_Short': 'MP_Short'})  # Renomeie se necessário

# Garantindo que ambas as tabelas tenham o mesmo número de linhas
assert len(tabela_long) == len(tabela_short) == 171, "As tabelas não têm 171 linhas."

# Método do cotovelo para determinar o número ideal de clusters
wss_long, wss_short = [], []
for k in range(1, 11):  # Testando de 1 a 10 clusters
    kmeans_long = KMeans(n_clusters=k, n_init=25, random_state=42)
    kmeans_long.fit(tabela_long[['Média_Ponderada']])
    wss_long.append(kmeans_long.inertia_)

    kmeans_short = KMeans(n_clusters=k, n_init=25, random_state=42)
    kmeans_short.fit(tabela_short[['Média_Ponderada']])
    wss_short.append(kmeans_short.inertia_)

# Filtro para o número de clusters a ser mostrado no gráfico
num_clusters = st.slider("Escolha o número de clusters para o gráfico", min_value=1, max_value=10, value=10)

# Plotando os gráficos WSS
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

ax[0].plot(range(1, num_clusters+1), wss_long[:num_clusters], marker='o', linestyle='-', color='b')
ax[0].set_title('Método do Cotovelo - Longo Prazo')
ax[0].set_xlabel('Número de Clusters')
ax[0].set_ylabel('Soma dos Erros Quadráticos (WSS)')

ax[1].plot(range(1, num_clusters+1), wss_short[:num_clusters], marker='o', linestyle='-', color='r')
ax[1].set_title('Método do Cotovelo - Curto Prazo')
ax[1].set_xlabel('Número de Clusters')
ax[1].set_ylabel('Soma dos Erros Quadráticos (WSS)')

st.pyplot(fig)

# Criando uma tabela de resumo para MP_Long por Data_Plantio e Municipio
df_summary_long = tabela.groupby(['Data_Plantio', 'Municipio'])['MP_Long'].sum().unstack().fillna(0)

# Criando o gráfico de barras empilhadas para MP_Long
fig_bar_long, ax_bar_long = plt.subplots(figsize=(12, 6))

# Usando uma paleta distinta para as cores da legenda
colors = plt.cm.tab20.colors  # 'tab20' possui 20 cores distintas para garantir variedade

df_summary_long.plot(kind='bar', stacked=True, ax=ax_bar_long, colormap='tab20')

# Personalizando o gráfico de MP_Long
ax_bar_long.set_title('MP_Long por Município e Data de Plantio')
ax_bar_long.set_xlabel('Data de Plantio')
ax_bar_long.set_ylabel('MP_Long')
ax_bar_long.tick_params(axis='x', rotation=45)  # Melhor legibilidade para o eixo X

# Adicionando os valores dentro das barras empilhadas com 2 casas decimais
for p in ax_bar_long.patches:
    height = p.get_height()
    width = p.get_width()
    x = p.get_x() + width / 2
    y = p.get_y() + height / 2
    ax_bar_long.annotate(f'{height:.2f}', (x, y), ha='center', va='center', color='black', fontsize=8)

# Movendo a legenda para fora do gráfico
ax_bar_long.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Municípios")

plt.tight_layout()

# Exibindo o gráfico de barras empilhadas para MP_Long
st.pyplot(fig_bar_long)

# Criando uma tabela de resumo para MP_Short por Data_Plantio e Municipio
df_summary_short = tabela.groupby(['Data_Plantio', 'Municipio'])['MP_Short'].sum().unstack().fillna(0)

# Criando o gráfico de barras empilhadas para MP_Short
fig_bar_short, ax_bar_short = plt.subplots(figsize=(12, 6))

# Usando uma paleta distinta para as cores da legenda
df_summary_short.plot(kind='bar', stacked=True, ax=ax_bar_short, colormap='tab20')

# Personalizando o gráfico de MP_Short
ax_bar_short.set_title('MP_Short por Município e Data de Plantio')
ax_bar_short.set_xlabel('Data de Plantio')
ax_bar_short.set_ylabel('MP_Short')
ax_bar_short.tick_params(axis='x', rotation=45)  # Melhor legibilidade para o eixo X

# Adicionando os valores dentro das barras empilhadas com 2 casas decimais
for p in ax_bar_short.patches:
    height = p.get_height()
    width = p.get_width()
    x = p.get_x() + width / 2
    y = p.get_y() + height / 2
    ax_bar_short.annotate(f'{height:.2f}', (x, y), ha='center', va='center', color='black', fontsize=8)

# Movendo a legenda para fora do gráfico
ax_bar_short.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Municípios")

plt.tight_layout()

# Exibindo o gráfico de barras empilhadas para MP_Short
st.pyplot(fig_bar_short)

# Exibindo a tabela mesclada para o município selecionado
municipio_selecionado = st.selectbox("Escolha o município", tabela['Municipio'].unique())
tabela_municipio = tabela[tabela['Municipio'] == municipio_selecionado]

# Função para colorir células nas colunas 'Chance_Long' e 'Chance_Short'
def colorir_celulas(val):
    if val == 'Alta':
        return 'background-color: green; color: white'
    elif val == 'Media':
        return 'background-color: orange; color: black'
    elif val == 'Baixa':
        return 'background-color: red; color: white'
    else:
        return ''

tabela_municipio.index = list(tabela_municipio['Data_Plantio'])

# Exibindo os dados do município selecionado com cores
st.write("### Dados com classificação de Chance")
st.dataframe(tabela_municipio.style.applymap(colorir_celulas, subset=['Chance_Long', 'Chance_Short']), use_container_width=True)
