import os
import platform
from datetime import datetime

import pandas as pd


def get_folder_content(path, file_suffixes):
    files_found = []
    created_datetimes = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(file_suffixes):
                full_file_path = os.path.join(root, file)
                print(f'Found {full_file_path}')
                files_found.append(file)
                created_ts = get_creation_date(full_file_path)
                created_datetimes.append(datetime.fromtimestamp(created_ts))
    df = pd.DataFrame({'file_name': files_found,
                       'created_datetime': created_datetimes, 'count': 1})
    df['file_type'] = df['file_name'].str.split('.', expand=True)[1]
    return df


def get_creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            print(('You seem to be on Linux, there is not easy way to get'
                   ' created date. We will settle for modified_date.'))
            return stat.st_mtime


def clean_file_name_suffix_and_drop_dupes(df, suffix):
    # Removes file type suffix
    df['file_name'] = df['file_name'].str.split('.', expand=True)[0]
    # Keeps file_name before suffix
    df['file_name'] = df['file_name'].str.split(suffix, expand=True)[0]
    df.drop_duplicates(subset='file_name', inplace=True)
    return df


def save_dataframe(df, output_directory, file_name='folder_content.csv'):
    output_file = os.path.join(output_directory, 'folder_content.csv')
    df.to_csv(output_file)


def get_raw_dir_content(folder_to_scrape, output_directory, output_name,
                        file_suffixes):
    files_in_folder = get_folder_content(folder_to_scrape, file_suffixes)
    save_dataframe(files_in_folder, output_directory, output_name)


def get_cleaned_dir_content(folder_to_scrape, output_directory, output_name,
                            file_suffixes, suffix_to_clean):
    files_in_folder = get_folder_content(folder_to_scrape, file_suffixes)
    cleaned_unique_objects_in_folder = clean_file_name_suffix_and_drop_dupes(
        files_in_folder, suffix_to_clean)
    save_dataframe(cleaned_unique_objects_in_folder, output_directory,
                   output_name)
