from selenium.webdriver.common.by import By
import time

from Common.kp_image_info_page import grab_image_info_page
from Common.regex_tools import make_text_edit_link, replace_to_comma
from Common.soup_tools import get_image_links

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'


def set_keywords_to_site(good_keywords, driver):
    driver.find_element(By.NAME, 'KeywordsRus').send_keys(good_keywords)
    driver.find_element(By.NAME, 'Add').click()


def end_selenium(driver):
    driver.close()
    driver.quit()


def go_my_images(link, keyword, driver) -> object:
    driver.get(link)
    html = driver.page_source
    return html


def check_keywords_number(keyword, driver):  # take number of images from site
    try:
        images_number = driver.find_element(By.CSS_SELECTOR,
                                            'body > table:nth-child(6) > tbody:nth-child(1) > '
                                            'tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > '
                                            'tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > '
                                            'b:nth-child(1)')
    except Exception as ex:
        print(f'{red}снимков с ключевым словом {green}{keyword}{end}{red} не найденно{end}\n'
              f'program terminated')
        exit()
    images_number = images_number.text
    images_number = int(images_number.replace(' ', ''))  # удаляю возможные пробелы перед преобразованием в целое число
    print(f'{green}{images_number} снимков с ключевым словом "{keyword}"{end}')
    keyword_link = driver.current_url[:-1]
    return keyword_link, images_number


def images_rotator(images_number, keyword_link, driver):
    range_number = images_number // 100 + 2  # количиство страниц выданных поиском
    # for x in range(1, range_number):  # главный цикл работы программы
    for x in range(2, 3):  # главный цикл работы программы
        link = f'{keyword_link}2&pg={x}'
        html = go_my_images(link, keyword='', driver=driver)  # получаю html  открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')

        for i in range(len(images_links)):  # (len(images_links)):
            text_edit_link, image_id, inner_id = make_text_edit_link(
                images_links[i].get('href'))  # generate edit image link
            image_id, caption, keywords = grab_image_info_page(driver, text_edit_link)  # grab info

            # if keywords not empty - optimise it
            if keywords != '':
                optimized_keywords = replace_to_comma(keywords)
