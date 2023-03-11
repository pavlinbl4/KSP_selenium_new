# удаление мусорных снимков по номеру съемки


import time
from selenium.webdriver.common.by import By
import re
from Common.authorization import autorization
from Common.create_XLXS_report_file import create_report
from Common.soup import get_soup
from Common.write_to_xlsx import write_to_xlsx
from KSP_shoot_create.find_images import find_images_by_id
from KSP_shoot_create.get_html import get_html_from_link
import sys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from Common.choose_input import chose_input


def get_image_links(html):
    soup = get_soup(html)
    table = soup.find_all('table')[9]
    tbody = table.find('tbody')
    return tbody.find_all(title="Добавить кадрировку")  # images_links


def make_text_edit_link(link):
    inner_id = re.findall(r'(?<=id=)\d+', link)[0]
    image_id = re.findall(r'(?<=photocode=)[^&]+', link)[0]
    image_edit_link = f'https://image.kommersant.ru/photo/archive/ViewPhoto.asp?ID={inner_id}&Lang=1&L=1'
    return image_edit_link, image_id, inner_id


def main_modul():
    path_to_file = create_report("Kommersant", "deleted_images", shoot_id, [shoot_id, "action"])
    deleted_count = 0
    link = find_images_by_id(shoot_id, browser)
    html = get_html_from_link(link, browser)  # получаю html открытой страницы
    images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
    number_of_shots = len(images_links)

    print(f'найдено {number_of_shots} снимков')
    if number_of_shots == 0:
        print("Program terminated")
        sys.exit()
    count = 0

    for i in range(number_of_shots):
        try:
            image_edit_link, image_id, inner_id = make_text_edit_link(images_links[i].get('href'))
            browser.get(image_edit_link)
            time.sleep(1)
            try:
                browser.find_element(By.CSS_SELECTOR, '.td-del > a:nth-child(1) > img').click()
                confirm = browser.switch_to.alert
                confirm.accept()

                count += 1
                write_to_xlsx(image_id, 'deleted', shoot_id, count, path_to_file)
                print(f'image {image_id} deleted')
                deleted_count += 1
            except NoSuchElementException:
                write_to_xlsx(image_id, "was published and can't be delete", shoot_id, count, path_to_file)
                print(f"Image {image_id} was published and can't be delete")
                continue
        except Exception as ex:
            print(ex)
    try:
        browser.close()
        browser.quit()

    except NoSuchWindowException:
        time.sleep(3)
        browser.close()
        browser.quit()

    print(f'удалено {deleted_count} снимков')


if __name__ == '__main__':
    shoot_id = chose_input()  # 'KSP_016180'

    browser = autorization()
    main_modul()
