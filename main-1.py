 #------------------------------------------Trabalho Prático I de Estatística e Probabilidade----------------------------------------------------#
#----------------------------------------Engenharia de Computação - Campus Coração Eucarístico--------------------------------------------------#
#-------------------------------------------------- PMG - Noite - G1/T1 - 2024/2----------------------------------------------------------------#
#---------------------------------------------------------Turma 82.27.101-----------------------------------------------------------------------#
#------------------------------------------------Alunos: Bruno Henrique Reis Almeida------------------------------------------------------------#
#----------------------------------------------------Cleber Marcos Pereira dos Reis-------------------------------------------------------------#
#------------------------------------------------------Gabriel da Silva Cassino-----------------------------------------------------------------#
#-----------------------------------------------Luiz Henrique Miranda Pacheco de Castro---------------------------------------------------------#
#-----------------------------------------------------------Orientações: -----------------------------------------------------------------------#

#Criado: 31-08-2024
#Revisao: 1_20_09_2024

#----->Instale o StreamLit:
#-->rode por favor pip install streamlit
import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------>Preparativos para acessar tabelas e o banco de dados MySQL no Python

#----->Instale o MySQL connector, se desejar transformar em
#-->banco de dados a tabela cedida pela professora, pórem use:
#-->rode por favor pip install mysql-connector-python
#-->Dica: rodar pip install mysql-connector é possível,
#-->pode dar erro de caching_sha2_password mesmo se
#-->alterar para mysql_native_password, o Python não
#consegue perceber a mudança


#----->Instale o Pandas, se não o possuir no PC:
#-->rode por favor
import pandas as pd

#importar as credenciais guardadas do MySQL
#para instalar: pip install toml
import toml

#rode pip install os
import os

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------>Preparativos para gerar tabelas e gráficos no Python

#Microsoft Visual C++ 14.0 ou acima é necessário para evitar erros com as
# bibliotecas matplotlib e vega.
# Ele pode ser obtido a partir do "Microsoft C++ Build Tools":
# Por gentileza, acesse: https://visualstudio.microsoft.com/visual-cpp-build-tools/

#pip install matplotlib
import matplotlib.pyplot as plt
#ver site: https://www.w3schools.com/python/matplotlib_pyplot.asp
#https://docs.streamlit.io/develop/api-reference/charts

#pip install numpy
import numpy as np

#pip install openpyxl
import openpyxl

#----------------->Estudarei como instalar, as bibliotecas a seguir:
#pip install streamlit-vega-lite
#pip install vega
from streamlit_vega_lite import vega_lite_component, altair_component

#pip install plotly==5.24.0
import plotly.io
#vem junto com plotly
import plotly.figure_factory as ff
#vem junto com plotly
import plotly.express as px

#pip install scipy
import scipy

#pip install vega-datasets
#pip install altair
import altair as alt
#ver site: https://www.datacamp.com/tutorial/altair-in-python

#pip install seaborn #--------------------------->Revisão Gabriel
import seaborn as sns  #-------------------------->Revisão Gabriel


#-------------------------------------------------Carregando a base de dados em CSV/Excel/MySQL-------------------------------------------------#
#conexao MySQL:
#criar arquivo de credenciais se não existe, por parâmetros

#cache do streamlit
@st.cache_data
#st.cache_resource

#se CSV:
def data_upload_csv():
  df = pd.read_csv("Dataset salary 2024.csv")
  return df


#se Excel:
def data_upload_excel():
  df = pd.read_excel("Dataset salary 2024.xlsx")
  return df



#---------------------------------------------------------Executando as questões----------------------------------------------------------------#
#---------------------------------------------------------------Questão 1-----------------------------------------------------------------------#
def quest_1():
  st.write("""Questão 1\n
  Construa uma tabela de frequências, de forma adequada, para representar a variável salário_in_usd.\n""")

  # Se Excel:
  df2 = data_upload_excel()

  # Calcular o número de faixas (k) usando a Regra de Sturges, sendo n o tamanho da amostra
  n = len(df2['salary_in_usd'])
  k = int(1 + 3.322 * np.log10(n))

  # Determinar o menor e o maior valor da coluna salary_in_usd
  menor_valor = df2['salary_in_usd'].min()
  maior_valor = df2['salary_in_usd'].max()

  # Definir os limites das faixas manualmente
  faixas = np.linspace(menor_valor, maior_valor, k + 1)

  # Definir as faixas de salários
  faixas_salario = pd.cut(df2['salary_in_usd'],
                          bins=faixas,
                          include_lowest=True)

  # Calcular as frequências
  frequencia = faixas_salario.value_counts(sort=False)
  percentual = frequencia / frequencia.sum() * 100
  freq_acumulada = frequencia.cumsum()
  perc_acumulada = percentual.cumsum()

  # Ajustar o valor da última célula da frequência relativa acumulada para 100%
  perc_acumulada.iloc[-1] = 100.0

  # Extrair os limites inferiores e superiores das faixas
  limites_inferiores = [
      interval.left for interval in faixas_salario.cat.categories
  ]
  limites_superiores = [
      interval.right for interval in faixas_salario.cat.categories
  ]

  # Construir a coluna com as faixas de salário
  faixas = [
      f"{inf} |-- {sup}"
      for inf, sup in zip(limites_inferiores, limites_superiores)
  ]

  # Tratar o último intervalo para incluir o limite superior
  faixas[-1] = f"{limites_inferiores[-1]} |--| {limites_superiores[-1]}"

  # Construir o DataFrame com as colunas necessárias
  dist_freq = pd.DataFrame({
      'Faixas de Salário (USD)':
      faixas,  # Nome personalizado para as faixas
      'Frequência Absoluta':
      frequencia.values,  # Garantindo apenas os valores
      'Frequência Relativa (%)':
      percentual.values,
      'Frequência Absoluta Acumulada':
      freq_acumulada.values,
      'Frequência Relativa Acumulada (%)':
      perc_acumulada.values
  })

  # Adicionar a linha "Total"
  total_frequencia_absoluta = frequencia.sum()
  total_frequencia_relativa = 100.0
  dist_freq.loc[len(dist_freq)] = [
      'Total', total_frequencia_absoluta, total_frequencia_relativa, '', ''
  ]

  # Exibir a tabela de frequências no Streamlit
  st.dataframe(data=dist_freq, use_container_width=True)


#---------------------------------------------------------------Questão 2-----------------------------------------------------------------------#
def quest_2():
  st.write("""Questão 2\n
  Construa uma tabela de frequências, de forma adequada, para representar a variável job_title.\n""")
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  frequencia = df2['job_title'].value_counts()
  percentual = df2['job_title'].value_counts(normalize=True) * 100

  #Construímos o DataFrame com a frequência
  #e o percentual:
  dist_freq_qualitativas = pd.DataFrame({
      'Frequência': frequencia,
      'Frequência relativa (%)': percentual
  })

  # Adicionar a linha "Total"
  total_frequencia = frequencia.sum()
  total_percentual = 100.0
  dist_freq_qualitativas.loc['Total'] = [total_frequencia, total_percentual]

  #Modelo 1
  #exibindo a tabela de frequências
  #Jobs = df2.groupby(['job_title'])['job_title'].count().reset_index(
  #name='Count').sort_values(['Count'])
  #st.dataframe(data=Jobs,hide_index=True)

  #teste
  #Modelo 2(em uso)
  #exibindo a tabela de frequências
  st.dataframe(
      data=dist_freq_qualitativas,
      column_config={"widgets": st.column_config.Column(width="medium")},
      use_container_width=True)


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------->Preparativos Questão 3
#------------------------------>Qualitativos(podem ser unidos por similaridade)
def get_3_a():
  # Se CSV:
  # df1 = data_upload_csv()
  # Se Excel:
  df2 = data_upload_excel()
  # ou MySQL:
  # df3 = data_upload_mysql()

  # Definir a ordem dos níveis da variável experience_level como categórica ordinal
  categorias_ordinais = ['Entry-level', 'Mid-level', 'Senior', 'Executive-level']
  df2['experience_level'] = pd.Categorical(df2['experience_level'],
                                            categories=categorias_ordinais,
                                            ordered=True)

  # Calcular a frequência e o percentual
  quest_3_plot_1 = df2['experience_level']
  frequencia_1 = quest_3_plot_1.value_counts().sort_index()  # Ordenar de acordo com a ordem categórica
  percentual_1 = quest_3_plot_1.value_counts(normalize=True).sort_index() * 100  # Mesma ordem

  # Construir o DataFrame com a frequência e o percentual
  dist_freq_quantitativas_tab_freq = pd.DataFrame({
      'Experience Level': frequencia_1.index,  # Tornar o índice uma coluna
      'Frequência': frequencia_1.values,
      'Porcentagem(%)': percentual_1.values
  })

  dist_freq_quantitativas_graf_barras = pd.DataFrame({
      'Frequência': frequencia_1,
  })

  st.write('experience_level - Análise')

  # Opções em subtópicos
  subtopic_graph = st.selectbox(
      'Tabelas e Gráficos',
      ['Selecione uma opção', 'Tabela de Frequência', 'Gráfico de Barras']
  )

  if subtopic_graph == 'Selecione uma opção':
      st.write(
          "Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico."
      )

  elif subtopic_graph == 'Tabela de Frequência':
      # Exibe a tabela
      st.write('experience_level - Tabela de Frequência')
      st.dataframe(
          dist_freq_quantitativas_tab_freq,
          column_config={"widgets": st.column_config.Column(width="medium")},
          use_container_width=True
      )

  elif subtopic_graph == 'Gráfico de Barras':
      # Exibe o Gráfico de Barras
      st.write('experience_level - Gráfico de Barras')
      st.bar_chart(dist_freq_quantitativas_graf_barras, 
                    x_label="Experience Level", 
                    y_label="Frequência absoluta")



#---------------->


import seaborn as sns
import matplotlib.pyplot as plt

def get_3_b():
  # Se CSV:
  # df1 = data_upload_csv()
  # Se Excel:
  df2 = data_upload_excel()
  # ou MySQL:
  # df3 = data_upload_mysql()

  quest_3_plot_2 = df2['employment_type']
  frequencia_2 = quest_3_plot_2.value_counts().sort_values(ascending=True)
  percentual_2 = quest_3_plot_2.value_counts(normalize=True) * 100

  # Construímos o DataFrame com a frequência e o percentual:
  dist_freq_quantitativas_2_tab_freq = pd.DataFrame({
      'Frequência': frequencia_2,
      'Porcentagem(%)': percentual_2
  })
  dist_freq_quantitativas_2_graf_barras = pd.DataFrame({'Frequência': frequencia_2})
  st.write('employment_type - Análise')

  # Opções em subtópicos
  subtopic_graph = st.selectbox('Tabelas e Gráficos', [
      'Selecione uma opção', 'Tabela de Frequência', 'Gráfico de Barras 1',
      'Gráfico de Barras 2'
  ])

  if subtopic_graph == 'Selecione uma opção':
      st.write(
          "Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico."
      )

  elif subtopic_graph == 'Tabela de Frequência':
      # Exibe a tabela
      st.write('employment_type - Tabela de Frequência')
      st.dataframe(
          dist_freq_quantitativas_2_tab_freq,
          column_config={"widgets": st.column_config.Column(width="medium")},
          use_container_width=True
      )

  elif subtopic_graph == 'Gráfico de Barras 1':
      # Exibe o Gráfico de Barras
      st.write('employment_type - Gráfico de Barras')
      st.bar_chart(dist_freq_quantitativas_2_graf_barras,
                    x_label="employment_type",
                    y_label="Frequência absoluta")

  elif subtopic_graph == 'Gráfico de Barras 2':
      # Exibe o Gráfico de Barras com seaborn e mostra os valores sobre as barras
      st.write('employment_type - Gráfico de Barras 2')

      fig, ax = plt.subplots()

      # Criando o gráfico de barras com seaborn
      sns.barplot(
          x=frequencia_2.index,  # Eixo X: categorias (employment_type)
          y=frequencia_2,        # Eixo Y: valores de frequência
          color="blue",          # Cor das barras
          ax=ax
      )

      # Adicionar título e rótulos dos eixos
      plt.title('employment_type\nGráfico de Barras v2')
      plt.ylabel('Frequência')
      plt.xlabel('Tipo de Vínculo Empregatício')

      # Adicionar os valores da frequência no topo de cada barra
      for p in ax.patches:
          ax.text(p.get_x() + p.get_width() / 2,   # Posição x
                  p.get_height(),                 # Posição y (altura da barra)
                  f'{int(p.get_height())}',       # Texto: o valor da frequência
                  ha='center', va='bottom')       # Alinhamento horizontal e vertical

      # Exibir o gráfico no Streamlit
      st.pyplot(fig)



#------------------------------------------>Revisão Gabriel - Fim


def get_3_c():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  quest_3_plot_3 = df2['company_size']
  st.write('company_size - Análise')
  frequencia_3 = quest_3_plot_3.value_counts().sort_values(ascending=True)
  percentual_3 = quest_3_plot_3.value_counts(normalize=True) * 100

  #Construímos o DataFrame com a frequência
  #e o percentual:
  dist_freq_quantitativas_tab_freq = pd.DataFrame({
      'Frequência': frequencia_3,
      'Porcentagem(%)': percentual_3
  })
  dist_freq_quantitativas_graf_barras = pd.DataFrame({
      'Frequência': frequencia_3,
  })
  #Opções em subtópicos
  subtopic_graph = st.selectbox(
      'Tabelas e Gráficos',
      ['Selecione uma opção', 'Tabela de Frequência', 'Gráfico de Barras'])
  if subtopic_graph == 'Selecione uma opção':
    st.write(
        "Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico."
    )
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('company_size- Tabela de Frequência')
    st.dataframe(
        dist_freq_quantitativas_tab_freq,
        column_config={"widgets": st.column_config.Column(width="medium")},
        use_container_width=True)
#---------------->
  elif subtopic_graph == 'Gráfico de Barras':
    st.write('company_size - Gráfico de Barras')
    #Exibe o Gráfico de Barras
    st.bar_chart(dist_freq_quantitativas_graf_barras, x_label="company_size",
                y_label="Frequência absoluta")


#------------------------------>Quantitativos(podem ser unidos por similaridade)
def get_3_d():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  quest_3_plot_4 = df2['salary_in_usd']
  st.write('salary_in_usd - Análise')
  frequencia_4 = quest_3_plot_4.value_counts().sort_values(ascending=True)
  percentual_4 = quest_3_plot_4.value_counts(normalize=True) * 100

  #Construímos o DataFrame com a frequência
  #e o percentual:
  dist_freq_quantitativas_4 = pd.DataFrame({
      'Frequência': frequencia_4,
      'Porcentagem(%)': percentual_4
  })
  #Opções em subtópicos
  subtopic_graph = st.selectbox('Tabelas e Gráficos', [
      'Selecione uma opção', 'Tabela de Frequência', 'Histograma'
  ])
  if subtopic_graph == 'Selecione uma opção':
    st.write(
        "Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico."
    )
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    quest_1()
  elif subtopic_graph == 'Histograma':
    #Em analise do melhor modelo
    st.write('salary_in_usd - Histograma')

    # Calcular o número de faixas (k) usando a Regra de Sturges, sendo n o tamanho da amostra
    n = len(df2['salary_in_usd'])
    k = int(1 + 3.322 * np.log10(n))

    # Determinar o menor e o maior valor da coluna salary_in_usd
    menor_valor = df2['salary_in_usd'].min()
    maior_valor = df2['salary_in_usd'].max()

    # Definir os limites das faixas manualmente
    faixas = np.linspace(menor_valor, maior_valor, k + 1)

    # Ajustar o primeiro limite inferior manualmente para ser 15000
    faixas[0] = 15000

    # Definir as faixas de salários para o histograma
    plt.figure(figsize=(10, 6))  # Ajuste o tamanho do gráfico
    hist_values, bin_edges, _ = plt.hist(df2['salary_in_usd'], bins=faixas, edgecolor='black', alpha=0.7)

    # Adicionar títulos e labels
    plt.title('Histograma da Distribuição de Salários em USD', fontsize=16)
    plt.xlabel('Faixas de Salário (USD)', fontsize=14)
    plt.ylabel('Frequência absoluta', fontsize=14)

    # Ajustar os valores do eixo x para os limites das faixas
    plt.xticks(bin_edges.round(2), rotation=45)  # Mostrar os limites inferiores e superiores no eixo x

    # Exibir as frequências e percentuais acima das barras
    for i in range(len(hist_values)):
        freq = int(hist_values[i])  # Frequência absoluta
        # Posição do texto: centro da barra no eixo x, e logo acima da barra no eixo y
        plt.text(bin_edges[i] + (bin_edges[i+1] - bin_edges[i]) / 2, 
                 hist_values[i], 
                 f'{freq}', 
                 ha='center', va='bottom', fontsize=10, color='black')

    # Exibir o gráfico no Streamlit
    st.pyplot(plt.gcf())


#---------------->


def get_3_e():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  quest_3_plot_5 = df2['remote_ratio']
  st.write('remote_ratio - Análise')
  frequencia_5 = quest_3_plot_5.value_counts()
  percentual_5 = quest_3_plot_5.value_counts(normalize=True) * 100
  #Construímos o DataFrame com a frequência
  #e o percentual:
  dist_freq_quantitativas_tab_freq = pd.DataFrame({
      'Frequência': frequencia_5,
      'Porcentagem(%)': percentual_5
  })
  dist_freq_quantitativas_graf_barras = pd.DataFrame({
      'Frequência': frequencia_5,
  })

  #Opções em subtópicos
  subtopic_graph = st.selectbox(
      'Tabelas e Gráficos',
      ['Selecione uma opção', 'Tabela de Frequência', 'Gráfico de Barras'])
  if subtopic_graph == 'Selecione uma opção':
    st.write(
        "Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico."
    )
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('remote_ratio - Tabela de Frequência')
    st.dataframe(
        dist_freq_quantitativas_tab_freq,
        column_config={"widgets": st.column_config.Column(width="medium")},
        use_container_width=True)
  elif subtopic_graph == 'Gráfico de Barras':
    #Exibe o Gráfico de Barras
    st.write('remote_ratio - Gráfico de Barras')
    st.bar_chart(dist_freq_quantitativas_graf_barras, x_label="remote_ratio",
                y_label="Frequência absoluta")


#---------------->


#---------------------------------------------------------------Questão 3-----------------------------------------------------------------------#
def quest_3():
  st.write("""Questão  3\n 
Construir um gráfico adequado para cada uma das seguintes variáveis:\n 
```
• experience_level             • Employment_type            • salary_in_usd\n
• remote_ratio                 • company_size\n
```           
Escreva um pequeno parágrafo citando os principais achados observados nos gráficos construídos."""
           )
  parts_quest_3()  #Para exibir por partes cada tópico


#Exibe por partes cada tópico
def parts_quest_3():

  #Opções dos tópicos
  graph_project = st.selectbox('Análises', [
      'Selecione uma opção', 'experience_level', 'employment_type',
      'company_size', 'salary_in_usd', 'remote_ratio', 'Parágrafo de resposta'
  ])
  if graph_project == 'Selecione uma opção':
    st.write("Ao escolher uma opção, será carregado o tópico desejado.")
  elif graph_project == 'experience_level':
    get_3_a()
  elif graph_project == 'employment_type':
    get_3_b()
  elif graph_project == 'company_size':
    get_3_c()
  elif graph_project == 'salary_in_usd':
    get_3_d()
  elif graph_project == 'remote_ratio':
    get_3_e()
  else:
    st.write("No que se refere à variável experience_level, é possível observar que a grande maioria dos desenvolvedores da amostra - cerca de 64,53% -  estão no nível Senior. Já com relação à variável employment_type, foi possível perceber que a esmagadora maioria dos desenvolvedores da amostra trabalhavam em tempo integral (99,5%). Com relação à variável company_size, constata-se que a grande maioria dos profissionais trabalham em empresas de porte médio (92,57%), sendo que, dentre os que não se encaixam nesse aspecto, a maioria faz parte de grandes empresas. No que se relaciona ao objeto de estudo principal, o salário, nota-se que a esmagadora maioria recebe entre 15000 USD e 329000 USD (92,59%), já que o número de profissionais que recebe mais do que isso é significativamente baixo com relação ao total. Por fim, a análise gráfica da variável remote_ratio mostra que grande parte dos desenvolvedores de dados não trabalham de forma remota (67,24%), e a a quantidade de programadores que trabalham 100% do tempo de forma remota é consideravelmente maior do que a quantidade de profissionais que trabalham on-line apenas metade do tempo.")


#---------------------------------------------------------------Questão 4-----------------------------------------------------------------------#
def quest_4():
  st.write("""Questão 4\n 
Calcule as medidas descritivas (média, mediana, mínimo, máximo, desvio padrão, coeficiente de variação, 1º quartil, 3º quartil) para a variável salário_in_usd.\n
Construir um boxplot para a variável salário_in_usd.\nEscreva um pequeno parágrafo citando as principais informações obtidas por meio da análise das medidas descritivas calculadas e do gráfico construído.""")
  #subtópicos da questão
  quest_4_topics()


def quest_4_topics():

  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  #Construir boxplot
  # Calcular a média aritmétia, mediana, variância e desvio-padrão
  salary = df2['salary_in_usd']
  # média,
  media = salary.mean()
  # mediana,
  mediana = salary.median()
  # mínimo,
  minimo = salary.min()
  # máximo,
  maximo = salary.max()
  # desvio padrão,
  desv_pad = np.std(salary)
  # coeficiente de variação,
  variancia = np.var(salary)
  # 1º quartil,
  q1 = salary.quantile(.25)
  # 3º quartil
  q3 = salary.quantile(.75)

  #Mostrar os resultados
  st.write('Medidas descritivas:')
  columns_r = [
      'Média', 'Mediana', 'Mínimo', 'Máximo', 'Desvio Padrão', 'Variância',
      '1º quartil', '3º quartil'
  ]
  lines = [media, mediana, minimo, maximo, desv_pad, variancia, q1, q3]
  results = pd.DataFrame({'Medidas': columns_r, 'Resultados': lines})
  # Plotar Boxplot
  st.dataframe(results, hide_index=True)
  st.write('Boxplot - salary_in_usd')
  #Criando figura
  fig = px.box(salary)
  st.plotly_chart(fig)
  st.write("""Parágrafo de resposta: \n 
  De acordo com a análise feita sobre as visualizações geradas para o salário em doláres, foi possível observar que existe uma pequena diferença positiva entre a média e a mediana, o que indica a existência de valores discrepantes que elevam a média da amostra. Essa observação foi confirmada ao observar o boxplot, já que ele apresentou uma alta quantidade de outliers positivos, ou seja, existem muitos profissionais recebendo um valor salarial acima do esperado. Ademais, foi aferido que o desvio padrão foi consideravelmente alto, o que indica uma grande variabilidade da remuneração dos desenvolvedores da amostra.""")

#---------------------------------------------------------------Questão 5-----------------------------------------------------------------------#
def quest_5():
  st.write("Questão 5")
  st.write("Construir uma tabela de contingência mostrando a frequência e um dos percentuais (da linha, da coluna OU do total geral) entre as variáveis experience_level e remote_ratio. Construa um gráfico adequado para representar os dados dessa tabela. Escreva um pequeno parágrafo citando os principais achados.")

  # Carregar dados (modifique conforme sua fonte de dados)
  df2 = data_upload_excel()  # ou data_upload_csv(), data_upload_mysql()

  # Tabela de contingência de frequências absolutas
  merge_crosstab = pd.crosstab(df2['experience_level'], 
                                df2['remote_ratio'], 
                                margins=True, 
                                margins_name="Total")

  # Renomear as colunas e adicionar rótulo para 'remote_ratio'
  merge_crosstab.columns = [f"{col} (%)" if col != "Total" else col for col in merge_crosstab.columns]
  merge_crosstab.index.name = "experience_level/remote_ratio"

  # Exibir a tabela de frequências absolutas
  st.write('Tabela de contingência: experience_level x remote_ratio - Frequências Absolutas')
  st.dataframe(merge_crosstab)

  # Tabela de contingência com porcentagens (normalizada)
  merge_crosstab2 = pd.crosstab(df2['experience_level'], 
                                df2['remote_ratio'], 
                                margins=True, 
                                margins_name="Total", 
                                normalize="all").mul(100).round(1)

  # Adicionar o símbolo de porcentagem às células (exceto na coluna 'Total')
  merge_crosstab2 = merge_crosstab2.map(lambda x: f"{x}%" if x != 'Total' else x)

  # Renomear colunas com o "%" e adicionar rótulos para 'remote_ratio'
  merge_crosstab2.columns = [f"{col} (%)" if col != "Total" else col for col in merge_crosstab2.columns]
  merge_crosstab2.index.name = "experience_level/remote_ratio"

  # Exibir a tabela de porcentagens
  st.write('Tabela de contingência: experience_level x remote_ratio - Porcentagens (%)')
  st.dataframe(merge_crosstab2)

  # Gráfico de barras empilhadas (frequência absoluta)
  st.write('Gráfico de Barras Empilhadas: experience_level x remote_ratio - Frequências absolutas')
  # Gerar a tabela de contingência sem as margens
  merge_crosstab3 = pd.crosstab(df2['experience_level'], df2['remote_ratio'], margins=False)

  # Adicionar o símbolo "%" nos valores de remote_ratio
  merge_crosstab3.columns = [f"remote_ratio = {col}%" for col in merge_crosstab3.columns]

  # Gerar o gráfico de barras empilhadas com as colunas renomeadas
  st.bar_chart(merge_crosstab3,
              x_label="Experience Level",
              y_label="Frequência Absoluta")
  st.write("Parágrafo de resposta: ")
  st.write("""Ao observar o gráfico de barras empilhadas, constata-se que, para todos os níveis de experiência, a maior parte dos desenvolvedores trabalha de forma totalmente presencial, seguida, respectivamente, pelo trabalho totalmente remoto, e, posteriormente, pelo trabalho parcialmente remoto. Além disso, percebe-se que 88,9% dos desenvolvedores estudados se encontram no nível intermediário ou sênior de experiência profissional.""")



#---------------------------------------------------------------Questão 6-----------------------------------------------------------------------#
def quest_6():
  st.write("""Questão 6 \n
  Construir uma tabela de contingência mostrando a frequência e um dos percentuais (da linha, da coluna OU do total geral) entre as variáveis Employment_type e company_size. Construa um gráfico adequado para representar os dados dessa tabela. Escreva um pequeno parágrafo citando os principais achados.""")
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  #fonte: acesse o site a seguir
  #https://acervolima.com/tabela-de-contingencia-em-python/
  #2 variáveis
  # Tabela de contingência de frequências absolutas
  merge_crosstab = pd.crosstab(df2['employment_type'], 
                                df2['company_size'], 
                                margins=True, 
                                margins_name="Total")

  merge_crosstab.index.name = "employment_type/company_size"

  # Exibir a tabela de frequências absolutas
  st.write('Tabela de contingência: employment_type x company_size - Frequências Absolutas')
  st.dataframe(merge_crosstab)

  # Tabela de contingência com porcentagens (normalizada)
  merge_crosstab2 = pd.crosstab(df2['employment_type'], 
                                df2['company_size'], 
                                margins=True, 
                                margins_name="Total", 
                                normalize="all").mul(100).round(1)

  # Adicionar o símbolo de porcentagem às células (exceto na coluna 'Total')
  merge_crosstab2 = merge_crosstab2.map(lambda x: f"{x}%" if x != 'Total' else x)

  merge_crosstab2.index.name = "employment_type/company_size"

  # Exibir a tabela de porcentagens
  st.write('Tabela de contingência: employment_type x company_size - Frequências relativas (%)')
  st.dataframe(merge_crosstab2)

  # Gráfico de barras empilhadas (frequência absoluta)
  st.write('Gráfico de Barras Empilhadas 1: employment_type x company_size - Frequências absolutas')
  # Gerar a tabela de contingência sem as margens
  merge_crosstab3 = pd.crosstab(df2['employment_type'],df2['company_size'], margins=False)

  merge_crosstab3.columns = [f"company_size = {col}" for col in merge_crosstab3.columns]

  # Gerar o gráfico de barras empilhadas com as colunas renomeadas
  st.bar_chart(merge_crosstab3,
              x_label="company_size",
              y_label="Frequência Absoluta")

  st.write("OBS: Para melhor visualização dos valores mínimos, utilize o scroll do mouse para aumentar a escala do gráfico")
  st.write("Parágrafo de resposta: ")
  st.write("""Ao analisar o gráfico gerado, percebe-se que a grande maioria dos desenvolvedores trabalha de 35h a 40h semanais - Full-Time, sendo que, desses profissionais, a maior parte está nas empresas de médio porte, seguida, respectivamente, pelas companhias de grande porte, e pelas de pequeno porte. Para os profissionais que atuam em outras modalidades de trabalho, constata-se que as diferenças entre as frequências relativas ao total, em porcentagem, giram em torno de 0,1% ou menos, ou seja, tais distribuições são relativamente uniformes.""")


#---------------------------------------------------------------Questão 7-----------------------------------------------------------------------#
def quest_7():
  st.write("""Questão 7\n
  Calcule as medidas descritivas (média, mediana, mínimo, máximo, desvio padrão, coeficiente
de variação, 1º quartil, 3º quartil) para a variável salário_in_usd estratificando pela variável
experience_level. Construir um boxplot estratificado entre essas duas variáveis. Escreva um pequeno
parágrafo citando as principais informações obtidas por meio da análise das medidas descritivas
calculadas e do gráfico construído (compare as medianas, a variabilidade, a homogeneidade, a
presença de valores discrepantes e as médias).""")

  # Carregar o arquivo Excel
  df2 = data_upload_excel()

  # Converter a variável experience_level em categórica ordinal, se não estiver
  categorias_ordinais = ['Entry-level', 'Mid-level', 'Senior', 'Executive-level']
  df2['experience_level'] = pd.Categorical(df2['experience_level'],
                                            categories=categorias_ordinais,
                                            ordered=True)

  # Função para calcular o coeficiente de variação
  def coeficiente_variacao(series):
      return (series.std() / series.mean()) * 100

  # Agrupar por experience_level e calcular as medidas descritivas
  medidas_descritivas = df2.groupby('experience_level')['salary_in_usd'].agg(
      média='mean',
      mediana='median',
      mínimo='min',
      máximo='max',
      desvio_padrão='std',
      coeficiente_variação=lambda x: coeficiente_variacao(x),
      primeiro_quartil=lambda x: x.quantile(0.25),
      terceiro_quartil=lambda x: x.quantile(0.75)
  ).reset_index()

  # Exibir as medidas descritivas no Streamlit
  st.write("Medidas Descritivas da variável salary_in_usd estratificadas por Nível de Experiência")
  st.dataframe(medidas_descritivas)

  # Construir o boxplot estratificado para salary_in_usd por experience_level
  fig = px.box(df2, 
                 x='experience_level', 
                 y='salary_in_usd', 
                 title="Boxplot: Salário (USD) por Nível de Experiência",
                 labels={"experience_level": "Nível de Experiência", "salary_in_usd": "Salário (USD)"},
                 category_orders={"experience_level": categorias_ordinais})  # Define a ordem das categorias

  st.plotly_chart(fig)

  st.write("Parágrafo de resposta:")
  st.write("""No que se refere às medias dos salários agrupados pelos diferentes níveis de experiência, observa-se que são alinhados do menor para o maior, partindo do Entry-level, seguido, respectivamente, por Mid-level, Senior e Executive-level. No que tange à mediana, ela apresenta a mesma ordem das médias para os níveis de experiência. Entretanto, destacam-se as diferenças entre a mediana e a média dos salários dos profissionais dos níveis intermediário e sênior. Em conformidade com isso, foi possível observar uma alta quantidade de valores discrepantes de remuneração para os desenvolvedores dos níveis anteriormente citados. Com relação à variabilidade, o desvio padrão dos salários apresenta maiores valores para os níveis intermediário e executivo, e o coeficiente de variação apresenta maiores valores para o nível de entrada e intermediário. Sendo assim, os níveis que apresentam maior variação são o o executivo, intermediário e sênior, dado que o desvio padrão desses é alto, e essa métrica é confiável para a extração da variabilidade. Por fim, o nível de entrada é o que apresenta maior homogeneidade entre os demais, já que ele obteve o menor desvio padrão.""")



#---------------------------------------------------------------Questão 8-----------------------------------------------------------------------#
def quest_8():
  st.write("""Questão 8\n
Calcule as medidas descritivas (média, mediana, mínimo, máximo, desvio padrão, coeficiente de variação, 1º quartil, 3º quartil) para a variável salário_in_usd estratificando pela variável Employment_type. Construir um boxplot estratificado entre essas duas variáveis. Escreva um pequeno parágrafo citando as principais informações obtidas por meio da análise das medidas descritivas calculadas e do gráfico construído (compare as medianas, a variabilidade, a homogeneidade, a presença de valores discrepantes e as médias).""")
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  # Função para calcular o coeficiente de variação
  def coeficiente_variacao(series):
      return (series.std() / series.mean()) * 100

  # Agrupar por experience_level e calcular as medidas descritivas
  medidas_descritivas = df2.groupby('employment_type')['salary_in_usd'].agg(
      média='mean',
      mediana='median',
      mínimo='min',
      máximo='max',
      desvio_padrão='std',
      coeficiente_variação=lambda x: coeficiente_variacao(x),
      primeiro_quartil=lambda x: x.quantile(0.25),
      terceiro_quartil=lambda x: x.quantile(0.75)
  ).reset_index()

  # Exibir as medidas descritivas no Streamlit
  st.write("Medidas Descritivas da variável salary_in_usd estratificadas por Tipo de Vínculo Empregatício:")
  st.dataframe(medidas_descritivas)

  # Construir o boxplot estratificado para salary_in_usd por experience_level
  fig = px.box(df2, 
                 x='employment_type', 
                 y='salary_in_usd', 
                 title="Boxplot: Salário (USD) por Vínculo Empregatício",
                 labels={"experience_level": " Tipo de Vínculo Empregatício", "salary_in_usd": "Salário (USD)"})
  st.plotly_chart(fig)
  st.write("Parágrafo de resposta:")
  st.write("""A partir da análise das médias das remunerações de acordo com as diferentes modalidades trabalhistas, observa-se que as maiores médias iniciam-se em Full-time, seguidas, respectivamente, por Contract basis, Part time e Freelancer. No que tange às medianas, a ordem dos valores de acordo com as modalidades é a mesma das médias. Em relação à existência de outliers, a modalidade Full time é a que apresenta a maior quantidade comparada às demais. No que se refere à variabilidade, os profissionais da modalidade Contract basis apresentam maior desvio padrão e coeficiente de variação. Sendo assim, eles são os que possuem maior variabilidade de salário. Além disso, vale destacar a curiosidade de que a modalidade Full time apresenta maior desvio padrão do que a Freelancer, enquanto a Freelancer apresenta maior coeficiente de variação do que a Full time, quando apenas as observamos. Por fim, no quesito de homogeneidade, os profissionais Freelancers são os que apresentam a maior uniformidade em seus pagamentos, já que possuem o menor desvio padrão e o 3° menor coeficiente de variação.""")


#---------------------------------------------------------------Questão 9-----------------------------------------------------------------------#
def quest_9():  #-------------------------------------Revisão Gabriel - Início
  st.write("""Questão 9\n
Cite uma situação hipotética em que o gráfico de linhas seria adequado para representar tais dados. Quais informações podemos obter ao utilizar um gráfico de linhas?""")

  #Moda
  #Mediana
  #Média

  #------>Comentário da situação hipotética
  st.write("Resposta:")
  st.write(
      """Como o gráfico de linha visa gerar uma análise de tendência temporal, na base de dados cedida seria interessante avaliar a coluna 'work_year' ante as demais variáveis, como 'experience_level', 'employment_type', e 'job_title', dentre outras similares, uma vez que tal análise permitiria concluir qual é a tendência de modalidades de trabalho, nível de experiência e cargos ao longo do tempo. Nesse contexto, é possível usar tais informações para uma melhor tomada de decisão, como qual especialização seguir, ou qual vínculo empregatício adotar.""")
  st.write("""Gráfico da quantidade de profissionais em função do tempo, para diferentes níveis de experiência profissional:""")

  #------>Aplicação da situação hipotética
  df = data_upload_excel()
  merge_crosstab = pd.crosstab(df['work_year'],
                               df['experience_level'],
                               normalize="all").mul(100).round(1)
  st.line_chart(merge_crosstab,
                x_label='work_year',
                y_label='qtd. in experience_level')


#----------------------------------------------------Revisão Gabriel - Fim

#---------------------------------------------------------------Questão 10----------------------------------------------------------------------#


def quest_10():
  st.write("""Questão 10""")
  st.write("""Pesquise a respeito do uso de mapa de calor em tabelas. Quando ele deve ser usado? Qual sua utilidade/benefícios? Mostre um exemplo hipotético.\n""")
  st.write("""Um heatmap (ou mapa de calor) é uma representação gráfica de dados onde os valores são representados por cores.\nNesse sentido, esse recurso gráfico é usado para detectar a ocorrência ou não de um determinado comportamento de um dado em análise (tendências, padrões, anomalias), tornando visíveis os pontos onde há engajamento.\nNesse sentido, os mapas de calor em tabelas facilitam a visualização de dados complexos, onde existem muitos números, que podem ser difíceis de compreender à primeira vista.""")
  st.write("""Por exemplo, as equipes de produtos de um site podem usar os mapas de calor para testar como os usuários estão interagindo com um novo recurso ou priorizar correções de bugs, enquanto os designers de UX e UI podem usar os mapas de calor para medir a popularidade ou a aversão ao design de uma página e implementar alterações que facilitem a navegação dos clientes em seu site.(Hotjar, 2024)""")


  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()


  #data = df2['work_year'].correc(df2['employment_type'])



#------------------------------------------------------------------------------------------------------------------------------------------------#


#------------------------------------------------------Organizando o Front-End------------------------------------------------------------------#
#----------------->Executando Streamlit
def load_descricao():
  st.write("Engenharia de Computação - Campus Coração Eucarístico")
  st.write("PMG - Noite - G1/T1 - 2024/2")
  st.write("Trabalho desenvolvido para a matéria:")
  st.write("Estatítica e Probabilidade")
  st.write("Turma 82.27.101")
  st.write("Professor(a) responsável: Julienne Borges Fujii")
  st.write("Alunos: Bruno Henrique Reis Almeida")
  st.write("Gabriel da Silva Cassino")
  st.write("Tema Proposto:")
  st.write("Salário do desenvolvedor de dados em 2024")
  st.write("Analisando salários de desenvolvedores de dados em 2024")


def load_planilha_excel():
  st.write("Planilha cedida pela professora Julienne Borges Fujii")

  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2 = data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  #escolha conforme desejar: df1,df2 ou df3(abaixo é apenas um exemplo)
  st.dataframe(data=df2)


#Menu Inicial
def main_page():
  st.sidebar.title('Menu')
  Page_Project = st.sidebar.selectbox('Questões', [
      'Descrição', 'Planilha Excel', 'Questão 1', 'Questão 2', 'Questão 3',
      'Questão 4', 'Questão 5', 'Questão 6', 'Questão 7', 'Questão 8',
      'Questão 9', 'Questão 10'
  ])

  if Page_Project == 'Descrição':
    load_descricao()
  elif Page_Project == 'Planilha Excel':
    load_planilha_excel()
  elif Page_Project == 'Questão 1':
    quest_1()
  elif Page_Project == 'Questão 2':
    quest_2()
  elif Page_Project == 'Questão 3':
    quest_3()
  elif Page_Project == 'Questão 4':
    quest_4()
  elif Page_Project == 'Questão 5':
    quest_5()
  elif Page_Project == 'Questão 6':
    quest_6()
  elif Page_Project == 'Questão 7':
    quest_7()
  elif Page_Project == 'Questão 8':
    quest_8()
  elif Page_Project == 'Questão 9':
    quest_9()
  elif Page_Project == 'Questão 10':
    quest_10()


#rode no terminal: streamlit run main.py

#criar arquivo de credenciais MySQL, se for usar banco de dados
#Passe os parãmetros para a função conforme for o seu banco de dados
#generate_toml('localhost',3306,'database','username','password','table')

#carrega a base no front-end, acesso o navegador no IP e Porta fornecidos no terminal
main_page()
