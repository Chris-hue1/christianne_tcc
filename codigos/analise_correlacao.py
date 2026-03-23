A2. Código em Python para Análise da Correlação
# Importando os módulos das bibliotecas
import pandas as pd
#  Carregando a planilha com as colunas de interesse
df = pd.read_excel("planilha_residuos.xlsx")
colunas_interesse = ['Animais', 'Sangue', 'Ossos', 'Resíduos abate','Resíduos Industria', 'Resíduos Descarte', 'Volume Captado',                     'Volume consumido', 'Volume Tratado', 'Eficiência', 'Recuperação de Tratamento', 'Perdas Híbridas', 'Energia']
df = df[colunas_interesse]
# Calculando a Correlação entre variáveis 
print("\nMatriz de correlação:")
print(df.corr(numeric_only=True))
desc1 = df.corr(numeric_only=True)
#Gerando planilha 
desc1.to_excel("planilha_correlacao.xlsx")
