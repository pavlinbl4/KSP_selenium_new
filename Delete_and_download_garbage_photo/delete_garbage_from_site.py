# удаление мусорных снимков по номеру съемки и резервное скачивание съемки на диск
import time
from selenium.webdriver.common.by import By
from Common.authorization import authorization
from Common.download_to_selected_folder import enable_download
from Common.get_html import get_html_from_link
from Common.make_page_link import make_shoot_edit_link
from Common.regex_tools import make_preview_photo_link
from Common.selenium_tools import find_images_by_id, end_selenium
from Common.soup_tools import get_image_links
import sys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from Common.choose_input import clipboard_or_input
from Common.tk_tools import select_folder_via_gui


def main_modul():
    shoot_id = clipboard_or_input()  # shoot_id = 'KSP_017892'

    # select folder to download images
    image_folder = select_folder_via_gui()
    download_dir = f'{image_folder}/{shoot_id}'


    # authorization on site and enable selected download folder
    driver = authorization()
    enable_download(driver, download_dir)

    # path_to_file = create_report("Kommersant", "deleted_images", shoot_id, [shoot_id, "action"])
    deleted_count = 0

    link = find_images_by_id(shoot_id, driver)
    html = get_html_from_link(link, driver)  # получаю html открытой страницы
    images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
    number_of_shots = len(images_links)

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
