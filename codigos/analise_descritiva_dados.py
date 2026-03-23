
# Importando os módulos das bibliotecas
import pandas as pd
#Carregando a planilha com as variáveis de interesse
df = pd.read_excel("planilha_residuos.xlsx")
colunas_interesse = ['Animais', 'Sangue', 'Ossos', 'Resíduos abate','Resíduos Industria', 'Resíduos Descarte' ,'Volume Captado','Volume consumido' ,'Volume Tratado','Eficiência', 'Recuperação de Tratamento' ,'Perdas Híbridicas' ,'Energia']
df = df[colunas_interesse]
# Calculando as estatísticas descritivas básicas por coluna
desc = df.describe(percentiles=[0.10, 0.25, 0.75, 0.90]).T
#Gerando planilha 
desc.to_excel("planilha_analise_descritiva.xlsx")
