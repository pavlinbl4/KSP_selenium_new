"""script download my published shoots to selected folder
pip install beautifulsoup4
pip install selenium
pip install lxml
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
from Common.authorization import authorization
from Common.choose_input import clipboard_or_input
from Common.download_to_selected_folder import enable_download
from Common.make_page_link import make_shoot_edit_link
from Common.notification import system_notification
from Common.soup_tools import get_image_links
from Common.selenium_tools import page_source_from_selenium
from Common.tk_tools import select_folder_via_gui


def main_cycle(images_number, driver, shoot_link):
    range_number = int(images_number) // 100 + 2  # количиство страниц выданных поиском
    for x in range(1, range_number):  # цикл по страницам съемки
        page_link = f'{shoot_link}2&pg={x}'  # ссылка на страницу с номером
        html = page_source_from_selenium(page_link, keyword=[], driver=driver)  # получаю html открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')
        for i in range(len(images_links)):  # (len(images_links)):
            shoot_edit_link = make_shoot_edit_link(images_links[i].get('href'))
            driver.get(shoot_edit_link)
            driver.find_element(By.CSS_SELECTOR,
                                f"div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()


def images_number_in_shot(driver):
    try:
        return int((driver.find_element(By.CSS_SELECTOR,
                                        'body > table:nth-child(6) '
                                        '> tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > '
                                        'table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > '
                                        'td:nth-child(1) > b:nth-child(1)').text).replace(' ', ''))
    except Exception as ex:
        print(ex)
        print('снимков с данным ключевым словом не найдено')
        return '0'


def create_folder(image_folder, shoot_id):
    os.makedirs(f'{image_folder}/{shoot_id}', exist_ok=True)


def find_images_on_site(driver, image_folder, shoot_id):  # авторизация гна главной странице
    driver.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)  # ввожу номер съемки
    select = Select(driver.find_element(By.NAME, 'ps'))
    select.select_by_value('100')
    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()
    driver.save_screenshot(f'{image_folder}/{shoot_id}/Screen_short_{shoot_id}.png')  # создаю скриншот для проверки
    return driver.current_url[:-1]  # return shoot link


def main():
    shoot_id = clipboard_or_input()
    image_folder = select_folder_via_gui()

    download_dir = f'{image_folder}/{shoot_id}'
    driver = authorization()
    shoot_link = find_images_on_site(driver, image_folder, shoot_id)  # авторизируюсь и получаю ссылку на данную съемку
    images_number = images_number_in_shot(driver)  # int число с количеством снимков в съемке
    enable_download(driver, download_dir)
    print(f'{images_number = }')
    main_cycle(images_number, driver, shoot_link)
    driver.close()
    driver.quit()
    system_notification(f'Work completed for shoot {shoot_id}', f'{images_number} files downloaded to {download_dir}')


if __name__ == '__main__':
    main()
