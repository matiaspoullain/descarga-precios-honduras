import requests
import os
from datetime import datetime
from lxml import html
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

# Diccionario de numero de mes a diccionario:
dict_calendario = {1: "Enero",
                   2: "Febrero",
                   3: "Marzo",
                   4: "Abril",
                   5: "Mayo",
                   6: "Junio",
                   7: "Julio",
                   8: "Agosto",
                   9: "Septiembre",
                   10: "Octubre",
                   11: "Noviembre",
                   12: "Diciembre"}



def get_current_year_month():
    current_year = datetime.now().year
    current_month_numero = datetime.now().month
    current_month_nombre = dict_calendario[current_month_numero]
    joined_current_year_month = '%20'.join([str(current_month_numero).zfill(2), str(current_month_nombre), str(current_year)])
    return current_year, current_month_numero, current_month_nombre, joined_current_year_month

def get_main_url(current_year):
    return f'http://historicos.simpah.hn/reportes_varios/index.php?dir=Reportes%20SIMPAH%20-%20{current_year}'

def get_local_directory_path(dict_reportes):
    lista_directorios = []

    for reporte in dict_reportes:
        for tipo in dict_reportes[reporte]:
            lista_directorios.append(os.path.join('data', 'pdfs', reporte, tipo))
    
    return lista_directorios



def get_list_reportes_tipo_urls(dict_reportes, main_url, joined_current_year_month):
    lista_urls_bases = []

    for reporte in dict_reportes:
        reporte_formateado = reporte.replace(' ', "%20").replace('é', '%C3%A9')
        for tipo in dict_reportes[reporte]:
            tipo_formateado = tipo.replace(' ', "%20").replace('é', '%C3%A9')
            url_it = os.path.join(main_url, reporte_formateado, joined_current_year_month, tipo_formateado)
            lista_urls_bases.append(url_it)
    
    return lista_urls_bases


def get_pdfs_urls_from_url(single_url):
    page = requests.get(single_url)
    tree = html.fromstring(page.content)

    pdfs_tree = tree.xpath('//a[@class="item file"]/@href')
    pdfs_urls = [f'http://historicos.simpah.hn/reportes_varios/{pdf_tree}' for pdf_tree in pdfs_tree]

    return(pdfs_urls)


def clean_glued_columns(df, columnas_num, columnas, bad_substring = ' '):
    for columna_num in columnas_num:
        if is_numeric_dtype(df[columna_num]):
            continue
        tiene_errores = df[columna_num].str.contains(bad_substring).values.tolist()
        tiene_errores = [lugar == True for lugar in tiene_errores]
        if sum(tiene_errores) > 0:
            indices_errores = np.where(tiene_errores)[0].tolist()
            for indice_error in indices_errores:
                indice_columna = columnas.index(columna_num)
                valor_mal = df.iloc[indice_error, indice_columna]
                valor_mal = ' '.join(valor_mal.split(bad_substring))
                valores_bien = valor_mal.split()
                for salto, nuevo_valor in enumerate(valores_bien):
                    df.iloc[indice_error, indice_columna + salto] = nuevo_valor
    return df

def clean_table(df, last_columns_n = 0):
    if (len(df.columns) == 1) & (last_columns_n > 0):
        df = df.loc[:, 0].str.split('\n', last_columns_n - 1, expand=True)
    #Nombres de columnas
    primera_linea = df.iloc[0, :].values.tolist()
    if 'Precios' not in primera_linea:
        return df
    indice_precios = primera_linea.index('Precios')
    if indice_precios == 0:
        columnas_char = ['Producto', 'Origen', 'Tamaño', 'Unidad de Venta']
    else:
        columnas_char = primera_linea[0:indice_precios]
    columnas_num = ['Precios_Rango_Bajo_Lempira', 'Precios_Rango_Alto_Lempira', 'Precios_RangoModa_Bajo_Lempira', 'Precios_RangoModa_Alto_Lempira']
    columnas = columnas_char + columnas_num

    #Remove first rows 
    df = df.iloc[4:, :].reset_index(drop = True)
    if len(df.columns) <= 6:
        n_new_cols = len(columnas) - len(df.columns)
        for i in range(n_new_cols):
            df[f'nueva_{i}'] = ''

    df.columns = columnas

    #Check if a numeric columns has spaces
    bad_substrings = ['\n ', ' ']
    for bad_substring in bad_substrings:
        df = clean_glued_columns(df, columnas_num, columnas, bad_substring = bad_substring)

    #Clean numeric columns:
    for columna in columnas_num:
        df[columna] = df[columna].astype(str)
        df.loc[:,columna] = pd.to_numeric(df.loc[:,columna].map(lambda x: x.replace(',', '').replace('None', '')))

    #Clean cheracter columns:
    for columna in columnas_char:
        df.loc[:,columna] = df.loc[:,columna].map(lambda x: x.replace('\n', '').replace('None', ''))
    
    return df

