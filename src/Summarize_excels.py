#Summarize unified excels

from src.diccionario_filtro_cultivos import cultivos_selectos

import pandas as pd
import os

unified_excel = os.path.join('data', 'excels', 'joined_excels', 'all_tables_together.xlsx')
total_df = pd.read_excel(unified_excel)

filtered_df = pd.DataFrame()
for parte_zona in cultivos_selectos:
    df_it = total_df[(total_df.Zona.str.contains(parte_zona)) & (total_df.Producto.isin(cultivos_selectos[parte_zona]))]
    break

df_it.Producto

prueba = total_df.Producto.unique()
prueba.sort()

total_df[(total_df.Zona.str.contains(parte_zona))]
total_df.columns
total_df['Zona']
