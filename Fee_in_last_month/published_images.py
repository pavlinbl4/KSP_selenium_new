from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.crome_options import setting_chrome_options
from scrap_publication_list import image_publications_voc
from checked_day_publications_only import checked_month_publications_only

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'

load_dotenv()
login = os.environ.get('login')
password = os.environ.get('password')
first_loggin = os.environ.get('first_loggin')

report_web_link = 'https://image.kommersant.ru/photo/archive/pubhistory.asp?ID='


def check_id_image(image_id):
    select = Select(driver.find_element(By.ID, "dt"))  # select "засыла"
    select.select_by_value("3")

    data_input = driver.find_element(By.ID, "since")
    data_input.clear()

    id_input = driver.find_element(By.ID, "code")
    id_input.clear()
    id_input.send_keys(image_id)

    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()

    return driver.page_source



def autorization(photographer):  # авторизация на главной странице
    driver.get(first_loggin)
    login_input = driver.find_element(By.ID, "login")
    login_input.send_keys(login)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".system input.but").click()
    driver.find_element(By.CSS_SELECTOR, '#au').send_keys(photographer)

def change_photographer(photographer):
    driver.get(first_loggin)
    driver.find_element(By.CSS_SELECTOR, '#au').clear()
    driver.find_element(By.CSS_SELECTOR, '#au').send_keys(photographer)


def select_today_published_images(check_date: str):
    locator = (By.CLASS_NAME, 'stxt')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    select = Select(driver.find_element(By.NAME, 'ps'))
    select.select_by_value('50')

    select = Select(driver.find_element(By.ID, "dt"))  # select "засыла"
    select.select_by_value("3")

    data_input = driver.find_element(By.ID, "since")
    data_input.clear()
    data_input.send_keys(check_date)

    data_input = driver.find_element(By.ID, "till")
    data_input.clear()
    data_input.send_keys(check_date)

    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()

    locator = (By.CLASS_NAME, 'stxt')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    return driver.page_source


def published_for_all_time(k):  # функция находит все опубликованные снимки из 'засыла' без фильтрации по датам
    report_link = f'{report_web_link}{k}#web'
    driver.get(report_link)
    report_html = driver.page_source
    publication_voc = \
        image_publications_voc(report_html)  # снимки из "засыла", которые были отмечены как опубликованные
    return publication_voc


def publication_info(k, count, check_date):
    publication_voc = published_for_all_time(k)  # получаю данные о всех публикациях данного снимка
    used_images = checked_month_publications_only(check_date, publication_voc, count)
    return used_images


driver = webdriver.Chrome(options=setting_chrome_options())

if __name__ == '__main__':
    # select_today_published_images('01.07.2023')
    change_photographer('Евгений Павленко')