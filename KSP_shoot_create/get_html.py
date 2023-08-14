def get_html_from_link(link, browser):
    browser.get(link)
    return browser.page_source
