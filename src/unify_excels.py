#Unify excels:

from src.utils import get_last_n_basedir
import pandas as pd
import os
from tqdm import tqdm

main_folder = os.path.join('data', 'excels')
out_folder = os.path.join(main_folder, 'joined_excels')
os.makedirs(out_folder, exist_ok=True)
out_total_file = os.path.join(out_folder, 'all_tables_together.xlsx')

excels_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(main_folder) for f in filenames if ((os.path.splitext(f)[1] == '.xlsx') & ('joined_excels' not in dp))]

total_df = pd.DataFrame()
for excel_file in tqdm(excels_files):
    zona_it = get_last_n_basedir(excel_file, 1)
    reporte_it = get_last_n_basedir(excel_file, 2)
    fecha_it = get_last_n_basedir(excel_file, 3)

    df_it = pd.read_excel(excel_file)
    df_it['Zona'] = zona_it
    df_it['Reporte'] = reporte_it
    df_it['Fecha'] = fecha_it

    total_df = pd.concat([total_df, df_it])

total_df.to_excel(out_total_file, index = False)
