import requests
import os
from datetime import datetime
from lxml import html

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



