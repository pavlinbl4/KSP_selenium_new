"""script download my published shoots to selected folder
pip install beautifulsoup4
pip install selenium
pip install lxml
"""

from selenium.webdriver.common.by import By
import os

from Common.download_to_selected_folder import enable_download
from Common.notification import system_notification
from Common.selenium_tools import find_all_images_on_site_by_shoot_id_or_keyword
from Common.soup_tools import get_image_links
from Common.tk_tools import select_folder_via_gui
from kp_selenium_tools.authorization import AuthorizationHandler


def make_shoot_edit_link(link):
    shoot_edit_link = f'https://image.kommersant.ru/photo{link[2:]}'
    return shoot_edit_link


def main_cycle():
    range_number = images_number // 100 + 2  # количиство страниц выданных поиском
    for x in range(1, range_number):  # цикл по страницам съемки
        page_link = f'{shoot_link}2&pg={x}'  # ссылка на страницу с номером
        html = go_my_images(page_link, keyword=[], driver=driver)  # получаю html открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')
        for i in range(len(images_links)):  # (len(images_links)):
            shoot_edit_link = make_shoot_edit_link(images_links[i].get('href'))
            driver.get(shoot_edit_link)
            driver.find_element(By.CSS_SELECTOR,
                                f"div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()


def images_number_in_shot():
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


def create_folder():
    os.makedirs(f'{image_folder}/{shoot_id}', exist_ok=True)


if __name__ == '__main__':
    shoot_id = input("input shoot id look like 'KSP_017***'\n")
    # shoot_id = "KMO_192663"
    image_folder = select_folder_via_gui()

    download_dir = f'{image_folder}/{shoot_id}'
    driver = AuthorizationHandler().authorize()
    shoot_link = find_all_images_on_site_by_shoot_id_or_keyword(shoot_id, driver,
                                                                only_kr=False)  # авторизируюсь и получаю ссылку на данную съемку
    images_number = images_number_in_shot()  # int число с количеством снимков в съемке
    enable_download()
    print(f'{images_number = }')
    main_cycle()
    driver.close()
    driver.quit()
    system_notification(f'Work completed for shoot {shoot_id}', f'{images_number} files downloaded to {download_dir}')
