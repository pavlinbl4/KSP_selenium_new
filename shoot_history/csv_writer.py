"""
Небольшая функция для записи csv файлов с возможностью задать имена колонок
"""

import csv
import os.path


def csv_writer(info, columns_name, csv_file_path):
    def write_csv_file(info, csv_file_path):
        with open(csv_file_path, 'a') as input_file:
            writer = csv.writer(input_file)
            writer.writerow(info)

    if os.path.exists(csv_file_path):
        write_csv_file(info, csv_file_path)
    else:
        info = columns_name
        write_csv_file(info, csv_file_path)


#
