from datetime import datetime
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from Common.authorization import autorization
from Common.notification import system_notification
from add_category import select_category
from checkbox_output import create_checkbox_dict
from input_window import get_input_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_shoot():
    today_date = f'{datetime.now().strftime("%d.%m.%Y")}'

    shoot_caption = get_input_data()  # add caption via GUI
    category_number = create_checkbox_dict()  # select category from GUI
    driver = autorization()
    try:

        driver.find_element(By.CSS_SELECTOR,
                            "body > table.logotbl > tbody > tr:nth-child(3)"
                            " > td > table > tbody > tr > td:nth-child(2) > a").click()
        driver.find_element(By.ID,
                            "nav_shoots_change").click()

        original_window = driver.current_window_handle

        # add category
        select_category(category_number, driver)

        driver.switch_to.window(original_window)  # focus in the main window after closing category window

        # добавляю описание съемки
        caption_input = driver.find_element(By.ID, "ShootDescription")
        caption_input.send_keys(shoot_caption)

        # ввожу дату
        day_input = driver.find_element(By.ID, "DateFrom")
        day_input.send_keys(today_date)

        time_input = driver.find_element(By.ID, 'TimeFrom')
        time_input.send_keys(Keys.NUMPAD1)

        time_input.send_keys(Keys.SPACE)

        time_input = driver.find_element(By.ID, 'TimeTo')
        time_input.send_keys(Keys.NUMPAD2)

        time_input.send_keys(Keys.SPACE)

        # выпадающее меню выбираю с помощью кнопок клавиатуры
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "CustomerContact")))
        customer_input = driver.find_element(By.ID, "CustomerContact")
        customer_input.send_keys("Павленко Евгений Валентинович")

        time.sleep(1)
        customer_input.send_keys(Keys.DOWN)
        customer_input.send_keys(Keys.ENTER)

        # выбираю бильдредактора с помощью класса Select
        select = Select(driver.find_element(By.NAME, 'EditorContactID'))
        select.select_by_value('2571')

        author_input = driver.find_element(By.ID, "AuthorContact")
        author_input.send_keys("Павленко Евгений Валентинович")
        time.sleep(1)
        author_input.send_keys(Keys.DOWN)
        time.sleep(1)
        author_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # confirm shoot creation
        driver.find_element(By.ID, 'SubmitBtn').click()

        number = driver.find_element(By.ID, "shootnum").text
        number = number.replace("№ ", "KSP_0")
        pyperclip.copy(number)

        system_notification(number, shoot_caption)

        driver.close()
        driver.quit()

        time.sleep(1)

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()


if __name__ == '__main__':
    create_shoot()
