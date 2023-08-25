from Common.authorization import autorization
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from KSP_shoot_create.checkbox_output import create_checkbox_dict


# def open_shoot_creation_page(driver):
#     driver.find_element(By.CSS_SELECTOR,
#                          "body > table.logotbl > tbody > tr:nth-child(3)"
#                          " > td > table > tbody > tr > td:nth-child(2) > a").click()
#     driver.find_element(By.ID,
#                          "nav_shoots_change").click()
#     return driver


def select_category(category_number, driver):
    wait = WebDriverWait(driver, 10)
    driver.execute_script("OpenPopupWindow('ShootSubjectsAdmin.asp')")
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    category = Select(driver.find_element(By.ID, 'SubjectID'))
    category.select_by_value(category_number)
    driver.find_element(By.XPATH, '//*[@id="addrow"]').click()
    driver.find_element(By.XPATH, '//*[@id="DivSubmit"]/input[1]').click()
    return driver

# def add_category_to_shoot():
#     category_number = create_checkbox_dict()
#     # browser = autorization()  # this only for test
#     # browser = open_shoot_creation_page(browser)   # this only for test
#     select_category(category_number, driver)


# if __name__ == '__main__':
#     add_category_to_shoot()
