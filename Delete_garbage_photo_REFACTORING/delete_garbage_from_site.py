# удаление мусорных снимков по номеру съемки

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
from os import getenv
import os.path


def main_modul():
    load_dotenv()
    login = getenv('login')
    password = getenv('password')
    first_loggin = getenv('first_loggin')

    shoot_id = 'KSP_017491'
    flag = 1
    deleted_count = 0

    file_path = f'/Volumes/big4photo-4/EDITED_JPEG_ARCHIV/Downloaded_from_fotoagency/{shoot_id}/delited_files.txt'

    options = webdriver.ChromeOptions()
    options.headless = True  # фоновый режим
    options.add_argument("--disable-blink-features=AutomationControlled")  # невидимость автоматизации
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    browser = webdriver.Chrome(options=options)

    def wtrite_to_txt_file(file_path, new_text):
        if os.path.exists(file_path):
            with open(file_path, 'a') as log_file:
                log_file.write(f"{new_text}\n")
        else:
            with open(file_path, 'w') as log_file:
                log_file.write(f"{new_text}\n")

    def autorization(shoot_id):  # авторизация гна главной странице

        browser.get(first_loggin)
        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys(login)
        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys(password)
        browser.find_element(By.CSS_SELECTOR, ".system input.but").click()
        browser.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)
        browser.find_element(By.CSS_SELECTOR, '#lib0').click()

        select = Select(browser.find_element(By.NAME, 'ps'))
        select.select_by_value('100')

        browser.find_element(By.CSS_SELECTOR, '#searchbtn').click()
        link = browser.current_url
        return link

    def go_my_images(link):
        browser.get(link)
        html = browser.page_source
        return html

    def get_image_links(html):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('table')[9]
        tbody = table.find('tbody')
        images_links = tbody.find_all(title="Добавить кадрировку")
        return images_links

    def get_keyword_of_image(link):
        browser.get(link)
        keywords = browser.find_element(By.ID, 'PhotoTextInfoControl1_Keywords').text
        return keywords

    def make_text_edit_link(link):
        inner_id = re.findall(r'(?<=id=)\d+', link)[0]
        text_edit_link = f'https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID={inner_id}&CloseForm=1'
        return text_edit_link

    for _ in range(2):
        link = autorization(shoot_id)  # закоментировал функции для спокойного анализа html
        html = go_my_images(link)  # получаю html  открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'найдено {len(images_links)} снимков')
        count = 0

        for i in range(len(images_links)):
            try:
                text_edit_link = make_text_edit_link(images_links[i].get('href'))
                int_photo_id = re.findall(r'(?<=ID=)\d+', text_edit_link)[0]
                browser.get(f'https://image.kommersant.ru/photo/archive/ViewPhoto.asp?ID={int_photo_id}&Lang=1&L=1')
                time.sleep(1)
                try:
                    browser.find_element(By.CSS_SELECTOR, '.td-del > a:nth-child(1) > img').click()
                    confirm = browser.switch_to.alert
                    confirm.accept()
                    time.sleep(5)
                    count += 1
                    wtrite_to_txt_file(file_path, f'image {int_photo_id} deleted')
                    print(f'image {int_photo_id} deleted')

                    deleted_count += 1
                except:
                    # print("cant delete image")
                    continue
            except Exception as ex:
                print(ex)
        browser.close()
        browser.quit()
        time.sleep(5)

    browser.close()
    browser.quit()
    print(f'удалено {deleted_count} снимков')


if __name__ == '__main__':
    main_modul()
