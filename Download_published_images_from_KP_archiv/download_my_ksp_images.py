"""script download my published shoots to selected folder
pip install beautifulsoup4
pip install selenium
pip install lxml
"""
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Common.download_to_selected_folder import enable_download
from Common.notification import system_notification
from Common.regex_tools import make_preview_photo_link
from Common.selenium_tools import find_all_images_on_site_by_shoot_id_or_keyword, page_source_from_selenium
from Common.soup_tools import get_image_links
from kp_selenium_tools.authorization import AuthorizationHandler
from loguru import logger

from kp_selenium_tools.gui_information import gui_information_for_work_for_downloading_images_from_kp_archive
from kp_selenium_tools.remove_image import delete_image_in_kp_photo_archive

logger.disable('__main__')


def make_shoot_edit_link(link):
    shoot_edit_link = f'https://image.kommersant.ru/photo{link[2:]}'
    return shoot_edit_link


def main_cycle():
    deleted_count = 0
    count = 0
    range_number = number_of_shots // 100 + 2  # количиство страниц выданных поиском
    for x in range(1, range_number):  # цикл по страницам съемки
        page_link = f'{link}2&pg={x}'  # ссылка на страницу с номером
        html = page_source_from_selenium(page_link, keyword=[], driver=driver)  # получаю html открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')
        for i in range(len(images_links)):  # (len(images_links)):
            preview_photo_window_link, image_id, inner_id = make_preview_photo_link(images_links[i].get('href'))
            shoot_edit_link = make_shoot_edit_link(images_links[i].get('href'))
            logger.info(shoot_edit_link)
            driver.get(shoot_edit_link)

            # click to download image
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    f"div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()

                # function to delete images
                driver.get(preview_photo_window_link)
                count, deleted_count = delete_image_in_kp_photo_archive(driver, count, image_id, deleted_count)
            except NoSuchElementException:
                print(f"Couldn't download and delite image {image_id}")
    print(f'deleted {deleted_count}')


if __name__ == '__main__':
    # get information from user about shoot id and download directory
    shoot_id, download_dir, keyword = gui_information_for_work_for_downloading_images_from_kp_archive()

    # authorization on site and enable selected download folder
    driver = AuthorizationHandler().authorize()
    enable_download(driver, download_dir)

    # shoot_link = find_all_images_on_site_by_shoot_id_or_keyword(shoot_id, driver, only_kr=True)  # авторизируюсь и получаю ссылку на данную съемку
    link, number_of_shots = find_all_images_on_site_by_shoot_id_or_keyword(driver, shoot_id, keyword=keyword,
                                                                           only_kr=True)
    logger.info(link)
    logger.info(number_of_shots)

    print(f'{number_of_shots = }')
    main_cycle()
    driver.close()
    driver.quit()
    system_notification(f'Work completed for shoot {shoot_id}', f'{number_of_shots} files downloaded to {download_dir}')
