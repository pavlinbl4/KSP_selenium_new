import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delete_image_in_kp_photo_archive(driver, count, image_id, deleted_count):
    try:
        # find red ring shortcut to delete image
        driver.find_element(By.CSS_SELECTOR, '.td-del > a:nth-child(1) > img').click()

        # Wait for the alert to be present and then accept it
        wait = WebDriverWait(driver, 10)
        alert = wait.until(EC.alert_is_present())
        alert.accept()

        time.sleep(1)

        count += 1
        print(f'image {image_id} deleted')
        deleted_count += 1
    except NoSuchElementException:
        print(f"Image {image_id} was published and can't be deleted")
    return count, deleted_count
