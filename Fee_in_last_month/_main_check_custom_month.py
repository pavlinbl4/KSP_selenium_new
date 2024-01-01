"""
1. в фотоархивве можно отсмотреть только историю "засыла" изображений
2. "засланное" изображение не всегда опубликовано, нужно проверить это отдельно
"""
from Common.selenium_tools import end_selenium
from Fee_in_last_month.remove_folder import delete_folder
from Fee_in_last_month.select_month import select_month
from Fee_in_last_month.user_home_folder import home
from published_images import autorization, select_today_published_images, change_photographer
from check_published_images import one_day_images_cycle
from images_links import get_image_links
from images_vocabulary import make_image_dict
import re
import os
from create_report_file import create_report_file
from datetime import datetime
from date_with_custom_month import custom_month_date
import time

from u_xlsx_writer import universal_xlsx_writer
from tqdm import tqdm, trange


def count_months_publications(html_folder: str, path_to_file: str, photographer: str) -> int:
    count = 0  # счетчик засланных снимков за весь месяц

    # all saved html files
    list_of_html = os.listdir(html_folder)

    for html_file in list_of_html:
        with open(f'{html_folder}/{html_file}', 'r') as file:
            html = file.read()
        images_links = get_image_links(html)  # список ссылок на "засланные" снимки в течении одного дня
        images_voc = make_image_dict(images_links)  # словарь из "внутреннего" id снимка и стандартного, внешнего id
        count = one_day_images_cycle(images_voc, re.findall(r'\d{2}.\d{2}.\d{4}', html_file)[0], path_to_file, count,
                                     photographer)
        print(f'{html_file} - {count = }')
    return count


def main_modul(photographer: str, month_n_int: int, current_year: int):
    months_name, check_date, days_in_month = custom_month_date(month_n_int, current_year)



    # 1 создаю папку для хранения html данных

    html_folder = home.add_subfolder_to_kommersant(f'FEE/{current_year}_{months_name}_fee/{photographer}_HTML')
    os.makedirs(html_folder, exist_ok=True)

    # 2. нужно пройтись по всем дням месяца и получить данные о "засланных" снимках

    path_to_month_report_file = create_report_file(months_name, html_folder, photographer)

    # 2.2  авторизируюсь на сайте and send photographers name
    change_photographer(photographer)

    # 3 на данном этапе сохраню все страницы для последующего анализа
    for day in range(1, days_in_month + 1):
        check_date = datetime(current_year, month_n_int, day).strftime("%d.%m.%Y")
        html = select_today_published_images(check_date)
        time.sleep(1)
        with open(f'{html_folder}/source_page_{check_date}.html', 'w') as file:
            file.write(html)
    # for test

    # html_folder = '/Volumes/big4photo/Documents/Kommersant/FEE/2023_September_fee/Александр Миридонов_HTML'
    # path_to_month_report_file = '/Volumes/big4photo/Documents/Kommersant/FEE/2023_September_fee/report_file_September.xlsx'
    # photographer = 'Александр Миридонов'

    # 4 перебираю сохраненные страницы
    count = count_months_publications(html_folder, path_to_month_report_file, photographer)


    columns_n = (
        'Name', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
        'November', 'December')

    universal_xlsx_writer(photographer,
                          columns_names=columns_n,
                          file_path=f'/Users/evgeniy/Documents/Kommersant/FEE/report.xlsx',
                          sheet_name=str(current_year),
                          row_line=photic_index,
                          column_number=month_n_int,
                          cell_data=count

                          )

    delete_folder(html_folder)  # delete folder with html files

    return count, months_name


if __name__ == '__main__':
    # set month number manually
    month_n_int = select_month()


    # month_n_int = month_number()  # int(input('input months number'))
    current_year =  2023   # int(input('input year'))
    driver = autorization('Евгений Павленко')

    camera_men = {
        2: 'Евгений Павленко',
        3: 'Владислав Лоншаков',
        4: 'Василий Дерюгин',
        5: 'Максим Кимерлинг',
        6: 'Александр Петросян',
        7: 'Александр Коряков',
        # 8: 'Александр Казаков',
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

        # в результате имеем фотографа и количество публикация за месяц

        # cycle for photographers in dict
        for photic_index, photic in tqdm(camera_men.items()):
            count, months_name = main_modul(photographer=photic, month_n_int=month_number, current_year=current_year)

        # photic_index = 16
        # count, months_name = main_modul(photographer='Дмитрий Лебедев', month_n_int=i)

    end_selenium(driver)
