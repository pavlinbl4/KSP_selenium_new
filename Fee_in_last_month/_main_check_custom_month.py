"""
1. в фотоархивве можно отсмотреть только историю "засыла" изображений
2. "засланное" изображение не всегда опубликовано, нужно проверить это отдельно
"""
from Common.selenium_tools import end_selenium
from Fee_in_last_month.read_data_from_html_files import read_information_from_html
from Fee_in_last_month.remove_folder import delete_folder
from Fee_in_last_month.select_month import select_month

from published_images import autorization, select_today_published_images, change_photographer
from create_report_file import create_report_file
from datetime import datetime
from date_with_custom_month import custom_month_date
import time

from tools.user_home_folder import HomeFolder
from u_xlsx_writer import universal_xlsx_writer
from tqdm import tqdm


def main_modul(photographer: str, month_n_int: int, current_year: int):
    months_name, check_date, days_in_month = custom_month_date(month_n_int, current_year)

    # 1 создаю папку для хранения html данных
    html_folder = HomeFolder(f'FEE/{current_year}_{months_name}_fee/{photographer}_HTML').add_subfolder()

    # 2. нужно пройтись по всем дням месяца и получить данные о "засланных" снимках
    path_to_month_report_file = create_report_file(months_name, html_folder, photographer)

    # 2.2  авторизуюсь на сайте and send photographers name
    change_photographer(photographer)

    # 3 на данном этапе сохраню все страницы для последующего анализа
    for day in range(1, days_in_month + 1):
        check_date = datetime(current_year, month_n_int, day).strftime("%d.%m.%Y")
        html = select_today_published_images(check_date)
        time.sleep(1)
        with open(f'{html_folder}/source_page_{check_date}.html', 'w') as file:
            file.write(html)

    # 4 read data from saved html pages
    count = read_information_from_html(html_folder, path_to_month_report_file, photographer)

    columns_n = (
        'Name', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
        'November', 'December')

    # 5 write date to xlsx file
    universal_xlsx_writer(photographer,
                          columns_names=columns_n,
                          file_path=f'/Users/evgeniy/Documents/Kommersant/FEE/report.xlsx',
                          sheet_name=str(current_year),
                          row_line=photic_index,
                          column_number=month_n_int,
                          cell_data=count

                          )

    # 6 delete folder with html files
    delete_folder(html_folder)  # delete folder with html files

    return count, months_name


if __name__ == '__main__':
    # set month number manually
    month_n_int = select_month()
    current_year = 2024  # int(input('input year'))
    driver = autorization('Евгений Павленко')

    camera_men = {
        2: 'Евгений Павленко',
        3: 'Владислав Лоншаков',
        4: 'Василий Дерюгин',
        5: 'Максим Кимерлинг',
        6: 'Александр Петросян',
        7: 'Александр Коряков',
        8: 'Александр Казаков',
        9: 'Дмитрий Духанин',
        10: 'Алексей Смагин',
        11: 'Глеб Щелкунов',
        12: 'Роман Яровицын',
        13: 'Александр Миридонов',
        14: 'Анатолий Жданов',
        15: 'Юрий Стрелец',
        16: 'Дмитрий Лебедев',
        17: 'Олег Харсеев'
    }

    for month_number in range(month_n_int, month_n_int + 1):

        # cycle for photographers in dict
        for photic_index, photic in tqdm(camera_men.items()):
            count, months_name = main_modul(photographer=photic, month_n_int=month_number, current_year=current_year)

    end_selenium(driver)
