from datetime import datetime
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from Common.authorization import autorization
from Common.notification import system_notification


def create_shoot():
    today_date = f'{datetime.now().strftime("%d.%m.%Y")}'
    shoot_caption = "Наружная реклама недвижимости"   #input("Введите описание съемки\n")
    browser = autorization()
    try:
        author_input = browser.find_element(By.CSS_SELECTOR, "input#au")
        author_input.send_keys("Евгений Павленко")

        browser.find_element(By.CSS_SELECTOR,
                             "body > table.logotbl > tbody > tr:nth-child(3)"
                             " > td > table > tbody > tr > td:nth-child(2) > a").click()
        browser.find_element(By.ID,
                             "nav_shoots_change").click()

        # добавляю описание съемки
        caption_input = browser.find_element(By.ID, "ShootDescription")
        caption_input.send_keys(shoot_caption)

        # ввожу дату
        day_input = browser.find_element(By.ID, "DateFrom")
        day_input.send_keys(today_date)

        time_input = browser.find_element(By.ID, 'TimeFrom')
        time_input.send_keys(Keys.NUMPAD1)

        time_input.send_keys(Keys.SPACE)

        time_input = browser.find_element(By.ID, 'TimeTo')
        time_input.send_keys(Keys.NUMPAD2)

        time_input.send_keys(Keys.SPACE)

        # выпадающее меню выбираю с помощью кнопок клавиатуры
        customer_input = browser.find_element(By.ID, "CustomerContact")
        customer_input.send_keys("Павленко Евгений Валентинович")
        time.sleep(1)
        customer_input.send_keys(Keys.DOWN)
        customer_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # выбираю бильдредактора с помощью класса Select
        select = Select(browser.find_element(By.NAME, 'EditorContactID'))
        select.select_by_value('2571')

        author_input = browser.find_element(By.ID, "AuthorContact")
        author_input.send_keys("Павленко Евгений Валентинович")
        time.sleep(2)
        author_input.send_keys(Keys.DOWN)
        time.sleep(2)
        author_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # window_before = browser.window_handles[0]
        browser.find_element(By.ID, 'SubmitBtn').click()
        # window_after = browser.window_handles[1]
        # browser.minimize_window()
        # browser.switch_to.window("main")
        browser.find_element(By.ID, 'SubmitBtn').click()
        # browser.minimize_window(window_after)
        # browser.switch_to.window(window_after)
        # browser.close()
        # browser.switch_to.window(window_befor)

        number = browser.find_element(By.ID, "shootnum").text
        number = number.replace("№ ", "KSP_0")
        pyperclip.copy(number)

        system_notification(number, shoot_caption)

        # time.sleep(1)

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    create_shoot()
