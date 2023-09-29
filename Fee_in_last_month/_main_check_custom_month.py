"""
1. в фотоархивве можно отсмотреть только историю "засыла" изображений
2. "засланное" изображение не всегда опубликовано, нужно проверить это отдельно
"""
from Common.selenium_tools import end_selenium
from Common.write_to_csv import csv_writer
from Fee_in_last_month.remove_folder import delete_folder
from Fee_in_last_month.user_home_folder import home
from ai_exel_writer import universal_xlsx_writer
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


def main_modul(photographer: str, month_n_int: int,):
    months_name, check_date, days_in_month, current_year = custom_month_date(month_n_int)

    # 2. нужно пройтись по всем дням месяца и получить данные о "засланных" снимках

    # 2.1 создаю папку для хранения html данных

    html_folder = home.add_subfolder_to_kommersant(f'FEE/{month_n_int}_{months_name}_fee/HTML')
    os.makedirs(html_folder, exist_ok=True)

    path_to_file = create_report_file(months_name, html_folder, photographer)

    # 2.2  авторизируюсь на сайте
    change_photographer(photographer)

    # 3 на данном этапе сохраню все страницы для последующего анализа
    for day in range(1, days_in_month + 1):
        check_date = datetime(current_year, month_n_int, day).strftime("%d.%m.%Y")
        html = select_today_published_images(check_date)
        time.sleep(1)
        with open(f'{html_folder}/source_page_{check_date}.html', 'w') as file:
            file.write(html)

    # 4 перебираю сохраненные страницы
    count = 0  # счетчик засланных снимков за весь месяц
    list_of_html = os.listdir(html_folder)
    for i in list_of_html:
        with open(f'{html_folder}/{i}', 'r') as file:
            html = file.read()
        images_links = get_image_links(html)  # список ссылок на "засланные" снимки в течении одного дня
        images_voc = make_image_dict(images_links)  # словарь из "внутреннего" id снимка и стандартного, внешнего id
        count = one_day_images_cycle(images_voc, re.findall(r'\d{2}.\d{2}.\d{4}', i)[0], path_to_file, count,
                                     photographer)
        print(f'{i} - {count = }')

    # save data about publication count to all cameraman
    csv_writer(
        (photographer, count),
        ('Фотограф', 'Количество опубликованных снимков'),
        f'/Volumes/big4photo/Documents/Kommersant/analiz_{months_name}.csv'
    )
    mont_photographer_dict = {photographer: count}

    universal_xlsx_writer(("Month",
                           'Евгений Павленко',
                  'Александр Коряков',
                  'Александр Петросян'),
                          [months_name,
                           mont_photographer_dict['Евгений Павленко'],
                           mont_photographer_dict['Александр Коряков'],
                           mont_photographer_dict['Александр Петросян']],
                          '/Volumes/big4photo/Documents/Kommersant/analiz_.xlsx',
                          'sheet_NAME')

    delete_folder(html_folder)  # delete folder with html files


if __name__ == '__main__':
    # month_n_int = month_number()  # int(input('input months number'))
    driver = autorization('Евгений Павленко')

    # camera_men = [
    #     'Евгений Павленко',
    #     'Марина Мамонтова',
    #     'Игорь Евдокимов',
    #     'Александр Чиженок',
    #     'Майя Жинкина',
    #     'Александр Петросян',
    #     'Александр Коряков',
    #     'Александр Казаков',
    #     'Дмитрий Духанин',
    #     'Алексей Смагин',
    #     'Глеб Щелкунов',
    #     'Роман Яровицын',
    #     'Александр Миридонов',
    #     'Анатолий Жданов',
    #     'Юрий Стрелец',
    #     'Дмитрий Лебедев',
    #     'Алексей Смышляев',
    # ]
    camera_men = ['Евгений Павленко',
                  'Александр Коряков',
                  'Александр Петросян']


    for photic in camera_men:
        print(f"{photic = }")
        main_modul(photographer=photic, month_n_int=9,)

    end_selenium(driver)

