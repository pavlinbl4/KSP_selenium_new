def get_html_from_link(link, driver):
    driver.get(link)
    return driver.page_source
