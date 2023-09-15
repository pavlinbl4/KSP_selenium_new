from Common.kp_image_info_page import image_info_optimization
from Common.make_page_link import make_history_link
from Common.regex_tools import make_text_edit_link
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from Common.soup_tools import get_image_links
import logging

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'


def open_page(page_link, browser):
    browser.get(page_link)


def work_to_history(driver):
    driver.find_element(By.ID, 'ctl00_MainContent_ShootInfoForm_FullShootNumber').click()
    driver.find_element(By.CLASS_NAME, 'history-header').click()
    first_link = driver.current_url
    full_link = make_history_link(first_link)  # получаю ссылку на страницу с подробной историей
    driver.get(full_link)  # открывается новая вкладка, нужно перейти на нее
    driver.switch_to.window(driver.window_handles[0])
    return driver.page_source


def find_images_by_id(shoot_id, driver):  # авторизация гна главной странице

    # driver.find_element(By.CSS_SELECTOR, '#au').clear()
    # driver.find_element(By.CSS_SELECTOR, '#au').send_keys('Евгений Павленко')

    driver.find_element(By.CSS_SELECTOR, '#code').clear()
    driver.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)
    driver.find_element(By.CSS_SELECTOR, '#lib0').click()
    select = Select(driver.find_element(By.NAME, 'ps'))
    select.select_by_value('100')
    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()
    link = driver.current_url
    return link


def end_selenium(driver):
    driver.close()
    driver.quit()


def set_keywords_to_site(good_keywords, driver):
    driver.find_element(By.NAME, 'KeywordsRus').clear()
    driver.find_element(By.NAME, 'KeywordsRus').send_keys(good_keywords)
    driver.find_element(By.NAME, 'Add').click()


def page_source_from_selenium(link, keyword, driver) -> object:
    driver.get(link)
    return driver.page_source


def check_keywords_number(keyword, driver):  # take number of images from site
    try:
        images_number_element = driver.find_element(By.CSS_SELECTOR,
                                                    'body > table:nth-child(6) > tbody:nth-child(1) > '
                                                    'tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > '
                                                    'tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > '
                                                    'b:nth-child(1)')

        images_number_element = images_number_element.text
        images_number = int(
            images_number_element.replace(' ', ''))  # удаляю возможные пробелы перед преобразованием в целое число
        print(f'{green}{images_number} снимков с ключевым словом "{keyword}"{end}')
        logging.info(f'{images_number} снимков с ключевым словом "{keyword}"')
        keyword_link = driver.current_url[:-1]
        return keyword_link, images_number
    except NoSuchElementException:
        logging.error(f'снимков с ключевым словом "{keyword}" не найдено')
        raise


# function to work with all images on all pages
def images_rotator(images_number, keyword_link, driver):
    range_number = images_number // 100 + 2  # количиство страниц выданных поиском
    # for x in range(1, range_number):  # главный цикл работы программы
    for x in range(1, 100):  # главный цикл работы программы переход по страницам архива
        link = f'{keyword_link}2&pg={x}'
        html = page_source_from_selenium(link, keyword='', driver=driver)  # получаю html открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')

        for i in range(len(images_links)):  # (len(images_links)):  # обработка каждого снимка на странице

            text_edit_link, image_id, inner_id = make_text_edit_link(
                images_links[i].get('href'))  # generate edit image link

            # optimise image info
            image_info_optimization(driver, text_edit_link)
