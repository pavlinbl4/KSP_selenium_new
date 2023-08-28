from bs4 import BeautifulSoup


def get_image_links(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.find_all('table')[9].find('tbody').find_all(title="Добавить кадрировку")


if __name__ == '__main__':
    get_image_links('/Volumes/big4photo/Documents/Kommersant/FEE/7_July_fee/HTML/source_page_13.07.2023.html')
