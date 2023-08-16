import os
import re

from Common.authorization import autorization
from Common.soup_tools import get_image_links
from Fee_in_last_month.check_published_images import one_day_images_cycle
from Fee_in_last_month.images_vocabulary import make_image_dict


def read_information_from_html(html_folder,path_to_file, photographer):
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


if __name__ == '__main__':
    driver = autorization()
    
    read_information_from_html('/Volumes/big4photo/Documents/Kommersant/FEE/7_July_fee/HTML',
                               '/Volumes/big4photo/Documents/Kommersant/FEE/7_July_fee/report_file_July_Евгений Павленко.xlsx',
                               'Pupkin')