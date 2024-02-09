# удаление мусорных снимков по номеру съемки и резервное скачивание съемки на диск
import time
from selenium.webdriver.common.by import By
from Common.choose_input import chose_input
from Common.download_to_selected_folder import enable_download
from Common.get_html import get_html_from_link
from Common.make_page_link import make_shoot_edit_link
from Common.regex_tools import make_preview_photo_link
from Common.selenium_tools import end_selenium, find_all_images_on_site_by_shoot_id_or_keyword
from Common.soup_tools import get_image_links
import sys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from Common.tk_tools import select_folder_via_gui
from kp_selenium_tools.authorization import AuthorizationHandler


def main_modul():
    shoot_id = chose_input()  # shoot_id = 'KSP_017892'
    # shoot_id = ''

    # select folder to download images
    image_folder = select_folder_via_gui()
    download_dir = f'{image_folder}/{shoot_id}'

    # authorization on site and enable selected download folder
    driver = AuthorizationHandler().authorize()
    enable_download(driver, download_dir)

    deleted_count = 0

    link, number_of_shots = find_all_images_on_site_by_shoot_id_or_keyword(driver, shoot_id, keyword='', only_kr=True)

    html = get_html_from_link(link, driver)  # получаю html открытой страницы
    images_links = get_image_links(html)  # получаю список ссылок редактирование изображения

    print(f'найдено {number_of_shots} снимков')
    if number_of_shots == 0:
        print("Program terminated")
        end_selenium(driver)
        sys.exit()
    count = 0

    for i in range(number_of_shots):

        try:
            preview_photo_window_link, image_id, inner_id = make_preview_photo_link(images_links[i].get('href'))

            # if I want to download image I must add here this function
            shoot_edit_link = make_shoot_edit_link(images_links[i].get('href'))
            driver.get(shoot_edit_link)
            driver.find_element(By.CSS_SELECTOR,
                                f"div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()

            # open preview image window
            driver.get(preview_photo_window_link)
            time.sleep(1)

            try:
                # find red ring shortcut to delete image
                driver.find_element(By.CSS_SELECTOR, '.td-del > a:nth-child(1) > img').click()
                confirm = driver.switch_to.alert
                confirm.accept()
                time.sleep(1)

                count += 1
                print(f'image {image_id} deleted')
                deleted_count += 1
            except NoSuchElementException:
                print(f"Image {image_id} was published and can't be delete")
                continue
        except Exception as ex:
            print(ex)
    try:
        # add sleep to  complete all started downloads
        time.sleep(5)
        end_selenium(driver)

    except NoSuchWindowException:
        time.sleep(3)
        end_selenium(driver)

    print(f'удалено {deleted_count} снимков')


if __name__ == '__main__':
    main_modul()
