from src.utils import *
from src.diccionario_reportes import dict_reportes
from tqdm import tqdm

print('Inicio de descarga de PDFs...')

current_year, current_month_number, current_month_nombre, joined_current_year_month = get_current_year_month()

main_url = get_main_url(current_year)

lista_urls = get_list_reportes_tipo_urls(dict_reportes, main_url, joined_current_year_month)
lista_directorio_local = get_local_directory_path(dict_reportes, current_month_number, current_year)

dict_links_pdfs = {}
for directory_path, single_url in zip(lista_directorio_local, lista_urls):
    dict_links_pdfs[directory_path] = get_pdfs_urls_from_url(single_url)

for directorio in tqdm(dict_links_pdfs):
    os.makedirs(directorio, exist_ok=True)
    for pdf_url in dict_links_pdfs[directorio]:
        archivo = os.path.basename(pdf_url)
        path_archivo = os.path.join(directorio, archivo)
        if os.path.exists(path_archivo):
            continue
        r = requests.get(pdf_url, allow_redirects=True)
        open(path_archivo, 'wb').write(r.content)

print('Descarga PDFs completas...')