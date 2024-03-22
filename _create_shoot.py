from datetime import datetime
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pyperclip
from Common.notification import system_notification
from Common.selenium_tools import select_category

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from KSP_shoot_create.start_window import get_input_data
from Telegramm_message.send_message_to_telegram import send_telegram_message
from ftp.ftp_follder import create_ftp_folder
from kp_selenium_tools.authorization import AuthorizationHandler


def navigate_to_shoot_creation_page(driver):
    driver.find_element("css selector",
                        "body > table.logotbl > tbody > tr:nth-child(3) > td > table > tbody > tr > td:nth-child(2) > a").click()
    driver.find_element('id', "nav_shoots_change").click()


def fill_shoot_details(driver, shoot_caption, category_number):
    original_window = driver.current_window_handle

    # Add category
    select_category(category_number, driver)
    driver.switch_to.window(original_window)  # Focus on the main window after closing the category window

    # Add shoot description
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(('id', "ShootDescription")))
    caption_input = driver.find_element('id', "ShootDescription")
    caption_input.send_keys(shoot_caption)


def set_shoot_date(driver, today_date):
    # ввожу дату
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(('id', "DateFrom")))
    day_input = driver.find_element('id', "DateFrom")
    day_input.send_keys(today_date)

    time_input = driver.find_element('id', 'TimeFrom')
    time_input.send_keys(Keys.NUMPAD1)

    time_input.send_keys(Keys.SPACE)
    time_input = driver.find_element('id', 'TimeTo')
    time_input.send_keys(Keys.NUMPAD2)
    time_input.send_keys(Keys.SPACE)


def set_customer(driver):
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(('id', "CustomerContact")))
    customer_input = driver.find_element('id', "CustomerContact")
    customer_input.send_keys("Павленко Евгений Валентинович")

    time.sleep(2)
    customer_input.send_keys(Keys.DOWN)
    customer_input.send_keys(Keys.ENTER)


def set_bildeditor(driver):
    # выбираю бильдредактора с помощью класса Select
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(("name", 'EditorContactID')))
    select = Select(driver.find_element("name", 'EditorContactID'))
    select.select_by_value('2571')


def set_author(driver):
    author_input = driver.find_element('id', "AuthorContact")
    author_input.send_keys("Павленко Евгений Валентинович")
    time.sleep(1)
    author_input.send_keys(Keys.DOWN)
    time.sleep(1)
    author_input.send_keys(Keys.ENTER)
    time.sleep(1)


def create_shoot():
    today_date = f'{datetime.now().strftime("%d.%m.%Y")}'

    # shoot_caption = get_input_data()  # add caption via GUI
    shoot_caption, category_number = get_input_data()  # add caption via GUI
    pyperclip.copy(shoot_caption)  # backup text to clipboard
    # category_number = create_checkbox_dict()  # select category from GUI
    driver = AuthorizationHandler().authorize()
    try:

        navigate_to_shoot_creation_page(driver)

        fill_shoot_details(driver, shoot_caption, category_number)

        set_shoot_date(driver, today_date)

        set_customer(driver)

        set_bildeditor(driver)

        set_author(driver)

        # confirm shoot creation
        driver.find_element('id', 'SubmitBtn').click()

        number = driver.find_element('id', "shootnum").text
        number = number.replace("№ ", "KSP_0")
        pyperclip.copy(number)

        create_ftp_folder(number)

        send_telegram_message(f'{number} - {shoot_caption}')

        system_notification(number, shoot_caption)

        driver.close()
        driver.quit()

        # time.sleep(1)

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()


if __name__ == '__main__':
    create_shoot()
