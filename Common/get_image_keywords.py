from selenium.webdriver.common.by import By


def get_keyword_of_image(link, driver):
    driver.get(link)
    keywords = driver.find_element(By.ID, 'PhotoTextInfoControl1_Keywords').text
    return keywords
