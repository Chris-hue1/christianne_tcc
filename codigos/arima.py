A5. Código em Python para as etapas da metodologia ARIMA na variável consumo de água
O código abaixo refere-se às etapas estacionariedade, identificação do modelo, diagnóstico dos resíduos e geração de previsões da variável energia. Para a variável água consumido foi usado o mesmo código porém onde encontra-se “serie = df["Energia"]”, é substituído por serie = df["Agua Consumida"].

# Importando Bibliotecas
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
from openpyxl import load_workbook
from openpyxl.chart import LineChart, BarChart, Reference
from statsmodels.stats.diagnostic import acorr_ljungbox

# 1. Realizando a leitura dos dados
# Lendo a planilha Excel contendo os dados da série temporal
df = pd.read_excel("planilha_residuos.xlsx")
# Criando uma coluna de data ao combinar ano e mês, fixando o dia como 01
df["data"] = pd.to_datetime(
    df["Ano"].astype(str) + "-" + df["Mês"].astype(str) + "-01"
)
# Ordenando os dados cronologicamente e definindo a coluna de data como índice
df = df.sort_values("data").set_index("data")
# Selecionando a série temporal de interesse (Energia)
serie = df["Energia"]

# 2. Fazendo a Diferenciação (d = 1)
# Aplicando a primeira diferença na série para torná-la estacionária
serie_diff = serie.diff().dropna()

# 3. Identificando ACF E PACF 
# Definindo o número máximo de defasagens com base no tamanho da série
n_lags = int(len(serie_diff) / 2) - 1
# Calculando a função de autocorrelação (ACF) da série diferenciada
acf_vals = acf(serie_diff, nlags=n_lags)
# Calculando a função de autocorrelação parcial (PACF) da série diferenciada
pacf_vals = pacf(serie_diff, nlags=n_lags, method="ywm")
# Criando um DataFrame para armazenar os valores da ACF
df_acf = pd.DataFrame({
    "Lag": np.arange(len(acf_vals)),
    "ACF": acf_vals
})
# Criando um DataFrame para armazenar os valores da PACF
df_pacf = pd.DataFrame({
    "Lag": np.arange(len(pacf_vals)),
    "PACF": pacf_vals
})

# 4. Ajustando Modelo Arima
# Definindo o modelo ARIMA com parâmetros (p=1, d=1, q=1)
modelo = ARIMA(serie, order=(1, 1, 1))
# Ajustando o modelo aos dados da série temporal
resultado = modelo.fit()
# Extraindo os resíduos do modelo ajustado
residuos = resultado.resid
# 5. Aplicando o teste de Ljung-Box para verificar autocorrelação dos resíduos
# em diferentes defasagens (lags)
ljung_box = acorr_ljungbox(
    residuos.dropna(),
    lags=[5, 10, 15, 20],
    return_df=True
)
# Definindo o nome do índice do DataFrame como "Lag"
ljung_box.index.name = "Lag"

# 5. Realizando diagnóstico ACF dos Resíduos
# Calculando a função de autocorrelação dos resíduos do modelo
acf_res = acf(residuos.dropna(), nlags=n_lags)
# Criando um DataFrame para armazenar a ACF dos resíduos
df_acf_res = pd.DataFrame({
    "Lag": np.arange(len(acf_res)),
    "ACF_Resíduos": acf_res
})

# 6. Exportando para para o excel
# Definindo o nome do arquivo Excel de saída
arquivo = "ARIMA_energia_Analise_Completa.xlsx"
# Criando um escritor Excel para salvar múltiplas abas no mesmo arquivo
with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:
    
    # Exportando a série original para uma aba
    serie.to_excel(writer, sheet_name="Serie_Original")
    # Exportando a série diferenciada para uma aba
    serie_diff.to_frame("Serie_Diferenciada").to_excel(
        writer, sheet_name="Serie_Diferenciada"
    )
    # Exportando os valores da ACF
    df_acf.to_excel(writer, sheet_name="ACF_Serie")
    # Exportando os valores da PACF
    df_pacf.to_excel(writer, sheet_name="PACF_Serie")
    # Exportando os resíduos do modelo
    residuos.to_frame("Resíduos").to_excel(writer, sheet_name="Resíduos")
    # Exportando a ACF dos resíduos
    df_acf_res.to_excel(writer, sheet_name="ACF_Resíduos")

# 7. Criando os gráficos no excel
# Abrindo o arquivo Excel gerado para inclusão dos gráficos
wb = load_workbook(arquivo)
# --- Gráfico ACF ---
# Selecionando a aba da ACF
ws = wb["ACF_Serie"]
# Criando um gráfico de barras para a ACF
graf_acf = BarChart()
graf_acf.title = "Correlograma da ACF – Série Diferenciada"
graf_acf.y_axis.title = "Autocorrelação"
graf_acf.x_axis.title = "Lag"
# Definindo o intervalo de dados para o gráfico
dados = Reference(ws, min_col=2, min_row=2, max_row=ws.max_row)
# Adicionando os dados ao gráfico
graf_acf.add_data(dados)
# Inserindo o gráfico na planilha
ws.add_chart(graf_acf, "E2")
# --- Gráfico PACF ---
# Selecionando a aba da PACF
ws = wb["PACF_Serie"]
# Criando um gráfico de barras para a PACF
graf_pacf = BarChart()
graf_pacf.title = "Correlograma da PACF – Série Diferenciada"
graf_pacf.y_axis.title = "Autocorrelação Parcial"
graf_pacf.x_axis.title = "Lag"
# Definindo o intervalo de dados
dados = Reference(ws, min_col=2, min_row=2, max_row=ws.max_row)
# Adicionando os dados ao gráfico
graf_pacf.add_data(dados)
# Inserindo o gráfico na planilha
ws.add_chart(graf_pacf, "E2")
# --- Gráfico Resíduos ---
# Selecionando a aba dos resíduos
ws = wb["Resíduos"]
# Criando um gráfico de linha para os resíduos
graf_res = LineChart()
graf_res.title = "Resíduos do Modelo ARIMA"
graf_res.y_axis.title = "Resíduos"
# Definindo o intervalo de dados
dados = Reference(ws, min_col=2, min_row=1, max_row=ws.max_row)
# Adicionando os dados ao gráfico com título
graf_res.add_data(dados, titles_from_data=True)
# Inserindo o gráfico na planilha
ws.add_chart(graf_res, "E2")
# --- Gráfico ACF dos Resíduos ---
# Selecionando a aba da ACF dos resíduos
ws = wb["ACF_Resíduos"]
# Criando um gráfico de barras para a ACF dos resíduos
graf_acf_res = BarChart()
graf_acf_res.title = "ACF dos Resíduos"
graf_acf_res.y_axis.title = "Autocorrelação"
graf_acf_res.x_axis.title = "Lag"
# Definindo o intervalo de dados
dados = Reference(ws, min_col=2, min_row=2, max_row=ws.max_row)
# Adicionando os dados ao gráfico
graf_acf_res.add_data(dados)
# Inserindo o gráfico na planilha
ws.add_chart(graf_acf_res, "E2")
# Salvando o arquivo Excel com os gráficos incluídos
wb.save(arquivo)

