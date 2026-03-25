import os
import pandas as pd

def mergeFiles():
    folder_path = os.getcwd()

    all_dataframes = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_excel(file_path)
            all_dataframes.append(df)

    merged_df = pd.concat(all_dataframes, ignore_index=True)

    merged_df.to_excel('avtoelon.xlsx', index=False)

    print('All excel files have been merged and saved')