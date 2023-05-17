"""
1. в фотоархивве можно отсмотреть только историю "засыла" изображений
2. "засланное" изображение не всегда опубликовано, нужно проверить это отдельно
"""
from Fee_in_last_month.remove_folder import delete_folder
from Fee_in_last_month.user_home_folder import home
from Fee_in_last_month.what_month import month_number
from published_images import autorization, end_selenium, select_today_published_images
from check_published_images import one_day_images_cycle
from images_links import get_image_links
from images_vocabulary import make_images_voc
import re
import os
from create_report_file import create_report_file
from datetime import datetime
from date_with_custom_month import custom_month_date






def main_modul(photographer):
    month_n_int = month_number()  # int(input('input months number'))
    months_name, check_date, days_in_month, current_year = custom_month_date(month_n_int)

    # 2. нужно пройтись по всем дням месяца и получить данные о "засланных" снимках

    # 2.1 создаю папку для хранения html данных

    html_folder = home.add_subfolder_to_kommersant(f'FEE/{month_n_int}_{months_name}_fee/HTML')
    os.makedirs(html_folder, exist_ok=True)

    path_to_file = create_report_file(months_name, html_folder, photographer)

    # 2.2  авторизируюсь на сайте
    autorization(photographer)

    # 3 на данном этапе сохраню все страницы для последующего анализа
    for day in range(1, days_in_month + 1):
        check_date = datetime(current_year, month_n_int, day).strftime("%d.%m.%Y")
        html = select_today_published_images(check_date)
        with open(f'{html_folder}/source_page_{check_date}.html', 'w') as file:
            file.write(html)

    # 4 перебираю сохраненные страницы
    count = 0  # счетчик засланных снимков за весь месяц
    list_of_html = os.listdir(html_folder)
    for i in list_of_html:
        with open(f'{html_folder}/{i}', 'r') as file:
            html = file.read()
        images_links = get_image_links(html)  # список ссылок на "засланные" снимки в течении одного дня
        images_voc = make_images_voc(images_links)  # словарь из "внутреннего" id снимка и стандартного, внешнего id
        count = one_day_images_cycle(images_voc, re.findall(r'\d{2}.\d{2}.\d{4}', i)[0], path_to_file, count)
        print(f'{i} - {count = }')

    end_selenium()
    delete_folder(html_folder)   # delete folder with html files


if __name__ == '__main__':
    # main_modul(photographer='Евгений Павленко')
    # main_modul(photographer='Александр Петросян')
    # main_modul(photographer='Александр Коряков')
    # main_modul(photographer='Александр Казаков')
    main_modul(photographer='Дмитрий Духанин')  # error  File "/Volumes/big4photo/_PYTHON/KSP_selenium_new/Fee_in_last_month/images_vocabulary.py", line 9
