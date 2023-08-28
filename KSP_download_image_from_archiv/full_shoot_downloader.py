"""This script download all images from fresh KP shoot"""

from Common.authorization import autorization
from Common.choose_input import chose_input
import time
from selenium.webdriver.common.by import By
from Common.regex_tools import full_shoot_html_link
from Common.selenium_tools import go_my_images
from Common.soup_tools import get_total_images


def download_one_page(number_of_downloads, shoot_id, page_link, count, driver):
    cgreen = '\33[0;32m'
    cend = '\033[0m'
    cred = '\033[91m'
    print(f'number_of_downloads - {number_of_downloads}')

    driver.get(page_link)

    for x in range(number_of_downloads):  # number_of_downloads
        index = ("0000" + str(count))[-5:]
        count += 1
        try:
            new_window = driver.window_handles[0]
            driver.switch_to.window(new_window)
            driver.find_element(By.CSS_SELECTOR,
                                f"#unselected_{shoot_id}_{index} > a.ui-icon.ui-icon-plus").click()
            time.sleep(4)

            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    "div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()
            except:
                driver.find_element(By.CSS_SELECTOR,
                                    "#AddPhotoImageControl1 > div.hi-panel > div > a").click()
            print(f'{cgreen}image {f"KSP_0{shoot_id}_{index}"} downloaded{cend}')

            driver.close()
        except Exception as ex:
            print(f'image {cred}{f"KSP_0{shoot_id}_{index}"}{cend} not aviable')


def main():
    shoot_id = chose_input()  # shoot_id = 'KSP_017892'
    page_link = full_shoot_html_link(shoot_id, page=0)
    driver = autorization()

    html = go_my_images(page_link, driver=driver, keyword=[])

    total_images = get_total_images(html)  # number of images in shoot
    print(total_images)

    count = 1
    if total_images <= 200:  # если количество снимков меньше 200 ( количество снимков на странице
        number_of_downloads = total_images  # количество скачиваний на странице с 200 картинками будет такое
        page = 1  # номер страницы с которой выкачиваю фото
        download_one_page(number_of_downloads, shoot_id, page_link, count, driver)
        # browser.close()
        driver.quit()

    else:  # если больше 200 снимков, то нужно будет открывать новые страницы
        pages_number = total_images // 200
        for page in range(1, pages_number + 2):
            if page != pages_number + 1:
                number_of_downloads = 200
            else:
                number_of_downloads = total_images % 200
            download_one_page(number_of_downloads, shoot_id, page, count, driver)
    print(f"скачивание завершено")


if __name__ == '__main__':
    main()
