

import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def delete_image_in_kp_photo_archive(driver,count, image_id, deleted_count):
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
    return count, deleted_count