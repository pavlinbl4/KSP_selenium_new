from selenium.webdriver.common.by import By


def get_keyword_of_image(link, browser):
    browser.get(link)
    keywords = browser.find_element(By.ID, 'PhotoTextInfoControl1_Keywords').text
    return keywords
