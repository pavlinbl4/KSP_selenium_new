"""script download my published shoots to selected folder
pip install beautifulsoup4
pip install selenium
pip install lxml
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
from Common.authorization import autorization
from Common.notification import system_notification
from tkinter import filedialog
from Common.soup_tools import get_image_links
from Common.selenium_tools import go_my_images


def select_folder():
    choose_folder = filedialog.askdirectory(
        initialdir='/Volumes/big4photo-4/EDITED_JPEG_ARCHIV/Downloaded_from_fotoagency',
        title="Select your Source directory")
    if len(choose_folder) > 0:
        return choose_folder
    else:
        print("You don't choose folder. Program terminated")
        exit()


def enable_download():
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)


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


def find_images_on_site():  # авторизация гна главной странице
    driver.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)  # ввожу номер съемки
    select = Select(driver.find_element(By.NAME, 'ps'))
    select.select_by_value('100')
    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()
    driver.save_screenshot(f'{image_folder}/{shoot_id}/Screen_short_{shoot_id}.png')  # создаю скриншот для проверки
    return driver.current_url[:-1]  # return shoot link


if __name__ == '__main__':
    shoot_id = input("input shoot id look like 'KSP_017***'\n")
    # shoot_id = "KMO_192663"
    image_folder = select_folder()
    # image_folder = '/Volumes/big4photo-4/EDITED_JPEG_ARCHIV/Downloaded_from_fotoagency'
    download_dir = f'{image_folder}/{shoot_id}'
    driver = autorization()
    shoot_link = find_images_on_site()  # авторизируюсь и получаю ссылку на данную съемку
    images_number = images_number_in_shot()  # int число с количеством снимков в съемке
    enable_download()
    print(f'{images_number = }')
    main_cycle()
    driver.close()
    driver.quit()
    system_notification(f'Work completed for shoot {shoot_id}', f'{images_number} files downloaded to {download_dir}')
