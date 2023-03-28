#Extract table from pdf:
#pip install camelot-py[cv] tabula-py
#sudo apt-get install python-tk
#conda install -c conda-forge ghostscript

from src.diccionario_filtro_cultivos import cultivos_selectos
from src.utils import get_current_year_month, get_last_n_basedir

import os
import pandas as pd
from tqdm import tqdm

print('Inicio procesamiento de excels...')

current_year, current_month_number, current_month_nombre, joined_current_year_month = get_current_year_month()
fecha_lab = f'{current_year}-{str(current_month_number).zfill(2)}'
main_folder = os.path.join('data', 'excels', fecha_lab)
excels_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(main_folder) for f in filenames if os.path.splitext(f)[1] == '.xlsx']

for excel_file in tqdm(excels_files):
    new_excel_file = excel_file.replace('excels', 'processed_excels')

    os.makedirs(os.path.dirname(new_excel_file), exist_ok=True)

    if os.path.exists(new_excel_file):
        continue
    
    #Get zona:
    zona_it = get_last_n_basedir(excel_file, 1)
    reporte_it = get_last_n_basedir(excel_file, 2).replace('Reportes- ', '')

    #Read excel:
    df_it = pd.read_excel(excel_file)

    for cultivo in cultivos_selectos:
        if cultivo not in zona_it:
            continue
        df_it = df_it[(df_it.Producto.isin(cultivos_selectos[cultivo]))]
        df_it.loc[df_it.Producto == 'Plátano verde', 'Unidad de Venta'] = df_it.loc[df_it.Producto == 'Plátano verde', 'Unidad de Venta'].map(lambda x: x.replace('(68-72 lb)', '(70 lb)'))
        break
    
    df_it['Mes'] = current_month_nombre
    df_it['Región'] = reporte_it

    #Unidad solo lo que esta dentro de la parentesis:
    df_it['Unidad de Venta'] = df_it['Unidad de Venta'].map(lambda x: x[x.find("(")+1:x.find(")")])

    #Seleccion y orden de columnas:
    df_it = df_it[['Producto', 'Mes', 'Unidad de Venta', 'Precios_Rango_Bajo_Lempira', 'Precios_Rango_Alto_Lempira', 'Región']]

    #Renombre de columnas
    df_it = df_it.rename(columns={"Producto": "Cultivo", "Unidad de Venta": "Unidad", 'Precios_Rango_Bajo_Lempira': 'Precio_Rango_Bajo', 'Precios_Rango_Alto_Lempira': 'Precio_Rango_Alto'})

    df_it.sort_values('Cultivo').reset_index(inplace=True, drop=True)

    #Save df as excel
    df_it.to_excel(new_excel_file, index=False)


print('Fin procesamiento de excels...')

