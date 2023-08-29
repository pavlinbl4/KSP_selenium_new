from bs4 import BeautifulSoup
import re

# pip install beautifulsoup4
# pip install lxml

def get_image_links(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[9]
    tbody = table.find('tbody')
    images_links = tbody.find_all(title="Добавить кадрировку")
    return images_links


def get_total_images(html):
    # get number of images in shoot from "просмотр съемки" page
    soup = BeautifulSoup(html, 'lxml')
    total_images = soup.find('span', id='ctl00_MainContent_AllPhoto1').text
    total_images = int(re.findall(r'\d+', total_images)[0])  # количество файлов в съемке
    return total_images


def get_soup(html):
    return BeautifulSoup(html, 'lxml')
