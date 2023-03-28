#Extract table from pdf:
#pip install camelot-py[cv] tabula-py
#sudo apt-get install python-tk
#conda install -c conda-forge ghostscript

from src.utils import clean_table, get_current_year_month

import camelot
import os
import pandas as pd
from lxml import html
from tqdm import tqdm

print('Inicio extracción de tablas de PDFs y su guardado como xlsx...')

current_year, current_month_number, current_month_nombre, joined_current_year_month = get_current_year_month()
fecha_lab = f'{current_year}-{str(current_month_number).zfill(2)}'
main_folder = os.path.join('data', 'pdfs', fecha_lab)
pdfs_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(main_folder) for f in filenames if os.path.splitext(f)[1] == '.pdf']

for pdf_file in tqdm(pdfs_files):
    excel_file = pdf_file.replace('pdfs', 'excels').replace('.pdf', '.xlsx')
    if os.path.exists(excel_file):
        continue
    #Read tables from pdf
    tables = camelot.read_pdf(pdf_file, pages = 'all')

    #Clean and unify tables
    df = pd.DataFrame()
    last_columns_n = 0
    for detected_table in tables:
        if len(detected_table.df) <= 4:
            continue
        cleaned_table = clean_table(detected_table.df, last_columns_n)
        last_columns_n = len(cleaned_table.columns)
        df = pd.concat([df, cleaned_table], axis = 0)

    #Create new folder:
    new_folder_path = os.path.dirname(pdf_file).replace('pdfs', 'excels')
    os.makedirs(new_folder_path, exist_ok=True)

    #Save df as excel
    df.to_excel(excel_file, index=False)

print('Tablas guardadas como xlsx...')


