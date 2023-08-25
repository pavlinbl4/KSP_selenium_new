# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from Common.authorization import autorization
#

# def find_images_by_id(shoot_id, driver):  # авторизация гна главной странице
#
#     driver.find_element(By.CSS_SELECTOR, '#au').clear()
#     driver.find_element(By.CSS_SELECTOR, '#au').send_keys('Евгений Павленко')
#
#     driver.find_element(By.CSS_SELECTOR, '#code').clear()
#     driver.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)
#     driver.find_element(By.CSS_SELECTOR, '#lib0').click()
#     select = Select(driver.find_element(By.NAME, 'ps'))
#     select.select_by_value('100')
#     driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()
#     link = driver.current_url
#     return link
#
#
# if __name__ == '__main__':
#     driver = autorization()
#     find_images_by_id('KSP_017270', driver)
#     driver.close()
#     driver.quit()
