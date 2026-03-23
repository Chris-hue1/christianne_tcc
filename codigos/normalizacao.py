A3. Código em Python para Normalização da tabela de Resíduos de Frigorífico de Suínos
# Importando os módulos das bibliotecas
import pandas as pd
from sklearn.preprocessing import StandardScaler
# Carregando a planilha 
df = pd.read_excel("planilha_residuos.xlsx")
#  Selecionando apenas colunas de interesse
colunas_interesse = ['Animais', 'Sangue', 'Ossos', 'Resíduos abate','Resíduos Industria', 'Resíduos Descarte','Volume Captado','Volume consumido', 'Volume Tratado', 'Eficiência', 'IRT','Perdas Híbridas','Energia']
df_num = df[colunas_interesse]
#  Normalizando com Z-score
scaler = StandardScaler()
df_norm = pd.DataFrame(scaler.fit_transform(df_num), columns=df_num.columns)
#  Juntando as colunas não-numéricas (ex: datas, categorias)
df_final = pd.concat([df.drop(columns=df_num.columns), df_norm], axis=1)
#  Gerando a planilha normalizada
df_final.to_excel("planilha_normalizada.xlsx", index=False)
