"""This script download all images from fresh KP shoot"""

import time
from selenium.webdriver.common.by import By

from Common.regex_tools import full_shoot_html_link, create_add_image_link
from Common.selenium_tools import page_source_from_selenium, end_selenium
from Common.soup_tools import get_total_images
from selenium.common.exceptions import NoSuchElementException

from kp_selenium_tools.authorization import AuthorizationHandler


def download_original_image(driver):
    # Скачивание либо оригинал снимка или уже добавленного в архив
    try:
        driver.find_element(By.CSS_SELECTOR,
                            "div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()
    except NoSuchElementException:
        driver.find_element(By.CSS_SELECTOR,
                            "#AddPhotoImageControl1 > div.hi-panel > div > a").click()


def rotate_all_images_in_shoot(total_images, shoot_id, driver):
    # Перебираю все снимки в съемке
    for count in range(1, total_images + 1):
        add_image_link = create_add_image_link(shoot_id, count)
        driver.get(add_image_link)

        # here can be any action with on add image page
        download_original_image(driver)


def main():
    # get shoot id
    shoot_id = chose_input()  # shoot_id = 'KSP_017892'

    #  generate html link "просмотр съемки"
    full_shoot_page_link = full_shoot_html_link(shoot_id, page=0)

    # select folder to download images
    image_folder = select_folder_via_gui()
    download_dir = f'{image_folder}/{shoot_id}'

    # authorization on site and enable selected download folder
    driver = AuthorizationHandler().authorize()
    enable_download(driver, download_dir)

    html = page_source_from_selenium(full_shoot_page_link, driver=driver, keyword=[])

    total_images = get_total_images(html)  # number of images in shoot

    # Основная функция которая перебирает все снимки в съемки
    rotate_all_images_in_shoot(total_images, shoot_id, driver)

    # Задержка для ожидания окончательной загрузки всех снимков
    time.sleep(10)

    end_selenium(driver)


if __name__ == '__main__':
    main()
