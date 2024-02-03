from datetime import datetime
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Common.notification import system_notification
from Common.selenium_tools import select_category

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from KSP_shoot_create.checkbox_output import create_checkbox_dict
from KSP_shoot_create.input_window import get_input_data
from kp_selenium_tools.authorization import AuthorizationHandler


def create_shoot():

    today_date = f'{datetime.now().strftime("%d.%m.%Y")}'

    shoot_caption = get_input_data()  # add caption via GUI
    pyperclip.copy(shoot_caption)  # backup text to clipboard
    category_number = create_checkbox_dict()  # select category from GUI
    driver = AuthorizationHandler().authorize()
    wait = WebDriverWait(driver, 30, poll_frequency=1)
    try:

        driver.find_element("css selector",
                            "body > table.logotbl > tbody > tr:nth-child(3)"
                            " > td > table > tbody > tr > td:nth-child(2) > a").click()
        driver.find_element('id',
                            "nav_shoots_change").click()

        original_window = driver.current_window_handle

        # add category
        select_category(category_number, driver)

        driver.switch_to.window(original_window)  # focus in the main window after closing category window

        # добавляю описание съемки
        caption_input = driver.find_element('id', "ShootDescription")
        wait.until(EC.element_to_be_selected(caption_input))
        caption_input.send_keys(shoot_caption)

        # ввожу дату
        day_input = driver.find_element('id', "DateFrom")
        wait.until(EC.element_to_be_selected(day_input))
        day_input.send_keys(today_date)

        time_input = driver.find_element('id', 'TimeFrom')
        time_input.send_keys(Keys.NUMPAD1)

        time_input.send_keys(Keys.SPACE)

        time_input = driver.find_element('id', 'TimeTo')
        time_input.send_keys(Keys.NUMPAD2)

        time_input.send_keys(Keys.SPACE)

        # выпадающее меню выбираю с помощью кнопок клавиатуры
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable(('id', "CustomerContact")))
        customer_input = driver.find_element('id', "CustomerContact")
        customer_input.send_keys("Павленко Евгений Валентинович")

        time.sleep(1)
        customer_input.send_keys(Keys.DOWN)
        customer_input.send_keys(Keys.ENTER)

        # выбираю бильдредактора с помощью класса Select
        select = Select(driver.find_element("name", 'EditorContactID'))
        select.select_by_value('2571')

        author_input = driver.find_element('id', "AuthorContact")
        author_input.send_keys("Павленко Евгений Валентинович")
        time.sleep(1)
        author_input.send_keys(Keys.DOWN)
        time.sleep(1)
        author_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # confirm shoot creation
        driver.find_element('id', 'SubmitBtn').click()

        number = driver.find_element('id', "shootnum").text
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
