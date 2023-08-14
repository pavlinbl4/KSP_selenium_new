from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
from Common.authorization import autorization
from Common.choose_input import chose_input
import time
from selenium.webdriver.common.by import By


def download_one_page(number_of_downloads, shoot_id, page_link, count, browser):
    cgreen = '\33[0;32m'
    cend = '\033[0m'
    cred = '\033[91m'
    print(f'number_of_downloads - {number_of_downloads}')

    browser.get(page_link
                )

    for x in range(number_of_downloads):  # number_of_downloads
        index = ("0000" + str(count))[-5:]
        count += 1
        try:
            new_window = browser.window_handles[0]
            browser.switch_to.window(new_window)
            browser.find_element(By.CSS_SELECTOR,
                                 f"#unselected_{shoot_id}_{index} > a.ui-icon.ui-icon-plus").click()
            time.sleep(4)

            new_window = browser.window_handles[1]
            browser.switch_to.window(new_window)
            try:
                browser.find_element(By.CSS_SELECTOR,
                                     "div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()
<<<<<<< HEAD
            except Exception as ex:
                browser.find_element(By.CSS_SELECTOR,
                                     "#AddPhotoImageControl1 > div.hi-panel > div > a").click()
                print(ex)
=======
            except:
                browser.find_element(By.CSS_SELECTOR,
                                     "#AddPhotoImageControl1 > div.hi-panel > div > a").click()
>>>>>>> origin/master
            print(f'{cgreen}image {f"KSP_0{shoot_id}_{index}"} downloaded{cend}')

            browser.close()
        except Exception as ex:
<<<<<<< HEAD
            print(ex)
=======
>>>>>>> origin/master
            print(f'image {cred}{f"KSP_0{shoot_id}_{index}"}{cend} not aviable')


def page_html(browser, page_link: str):
    browser.get(page_link)
    return browser.page_source


def get_total_images(html):
    soup = BeautifulSoup(html, 'lxml')
    total_images = soup.find('span', id='ctl00_MainContent_AllPhoto1').text
<<<<<<< HEAD
    return int(re.findall(r'\d+', total_images)[0])  # количество файлов в съемке
=======
    total_images = int(re.findall(r'\d+', total_images)[0])  # количество файлов в съемке
    return total_images
>>>>>>> origin/master


def get_login_password():
    load_dotenv()
    login = os.environ.get('login')
    password = os.environ.get('password')
    first_loggin = os.environ.get('first_loggin')
    return login, password, first_loggin


def make_html_link(shoot_id: str, page: int) -> str:
    splited_soot_id = shoot_id.split('_')
    return f'https://image.kommersant.ru/photo/wp/default.aspx?shootnum={splited_soot_id[1]}' \
           f'&sourcecode={splited_soot_id[0]}&pagesize=200&previewsize=128&page={str(page)}&nl=true&ord=F'


<<<<<<< HEAD
def main():
=======
if __name__ == '__main__':
    assert type(make_html_link('KSP_017605', 0)) == str
>>>>>>> origin/master
    shoot_id = chose_input()  # shoot_id = 'KSP_017892'
    page_link = make_html_link(shoot_id, page=0)
    browser = autorization()
    html = page_html(browser, page_link)
    total_images = get_total_images(html)  # number of images in shoot
    print(total_images)

    count = 1
    if total_images <= 200:  # если количество снимков меньше 200 ( количество снимков на странице
        number_of_downloads = total_images  # количество скачиваний на странице с 200 картинками будет такое
<<<<<<< HEAD
=======
        page = 1  # номер страницы с которой выкачиваю фото
>>>>>>> origin/master
        download_one_page(number_of_downloads, shoot_id, page_link, count, browser)
        # browser.close()
        browser.quit()

    else:  # если больше 200 снимков то нужно будет открывать новые страницы
        pages_number = total_images // 200
        for page in range(1, pages_number + 2):
            if page != pages_number + 1:
                number_of_downloads = 200
            else:
                number_of_downloads = total_images % 200
            download_one_page(number_of_downloads, shoot_id, page, count, browser)
    print(f"скачивание завершено")
<<<<<<< HEAD


if __name__ == '__main__':
    assert type(make_html_link('KSP_017605', 0)) == str
    main()

=======
>>>>>>> origin/master
