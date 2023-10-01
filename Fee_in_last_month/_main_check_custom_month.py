"""
1. в фотоархивве можно отсмотреть только историю "засыла" изображений
2. "засланное" изображение не всегда опубликовано, нужно проверить это отдельно
"""
from Common.selenium_tools import end_selenium
from Fee_in_last_month.remove_folder import delete_folder
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


def main_modul(photic_index, photographer: str, month_n_int: int):
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
    time.sleep(180)
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


    columns_n = (
        'Name', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
        'November', 'December')

    universal_xlsx_writer(photographer,
                          columns_names=columns_n,
                          file_path='/Users/evgeniy/Documents/Kommersant/FEE/report.xlsx',
                          sheet_name="2023",
                          row_line=photic_index,
                          column_number=month_n_int,
                          cell_data=count

                          )

    delete_folder(html_folder)  # delete folder with html files

    return count, months_name


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

    for i in range(8, 10):
        # camera_men = ('Евгений Павленко',
        #               'Александр Коряков',
        #               'Александр Петросян')
        camera_men = [
            'Евгений Павленко',
            'Владислав Лоншаков',
            'Василий Дерюгин',
            'Максим Кимерлинг',
            'Александр Петросян',
            'Александр Коряков',
            'Александр Казаков',
            'Дмитрий Духанин',
            'Алексей Смагин',
            'Глеб Щелкунов',
            'Роман Яровицын',
            'Александр Миридонов',
            'Анатолий Жданов',
            'Юрий Стрелец',
            'Дмитрий Лебедев',
            'Олег Харсеев',
        ]

        for photic_index, photic in enumerate(camera_men, 2):
            count, months_name = main_modul(photic_index, photographer=photic, month_n_int=i)
            time.sleep(60)

            # в результате имеем фотографа и количество публикация за месяц

    end_selenium(driver)
