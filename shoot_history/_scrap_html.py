from bs4 import BeautifulSoup
from get_file_extension import get_file_extension
from shoot_history.find_file_hdd import find_no_ext
from change_color_class import change_color_class_dng, change_color_class_raw
from colorama import Fore
from lost_files_to_csv import write_lost_files_info
from tkinter import filedialog, messagebox


def check_original_file_name(original_file_name,
                             my_date_format):  # проверяю был ли файл переименован по моим правилам или отправлен сразу с камеры
    if original_file_name.startswith("P"):
        original_file_name = my_date_format + original_file_name
    return original_file_name


def scrap_html(page_link, path):
    soup = BeautifulSoup(page_link, 'lxml')
    trs = soup.find('table', id='ProcessingGrid').find('tbody').find_all('tr')
    file_renames = {}

    trs_pub = soup.find('table', id='HistoryLogGrid').find('tbody').find_all('tr')

    komm_date = soup.find('tr', class_="row-alternating").find('td', class_="date-col").text[:10].split('.')
    my_date_format = komm_date[2] + komm_date[1] + komm_date[0]  # получаю дату передачи съемки

    for i in range(1, len(trs)):
        file_renames[trs[i].find('td').find_next('td').text[:-6]] = [trs[i].find('td').text[:-4]]

    for i in range(len(trs_pub)):
        xxx = trs_pub[i].find(class_="user-col").find_next('td').text
        if 'Добавлен:' in xxx:
            photo_id = trs_pub[i].find(class_="user-col").find_next('td').text[10:-2]  # id added image
            original_file_name = check_original_file_name(file_renames[photo_id][0], my_date_format)
            print(f"for file {photo_id} original filename is  {original_file_name}")
            file_renames[photo_id].append("ADDED")
            way_to_file = find_no_ext(original_file_name, path)  # function to find file on HDD
            if len(way_to_file) > 0:  # if file wasn't found
                extension = get_file_extension(way_to_file[0])  # originl_file_extension
                if extension in ['DNG', 'dng', 'JPG', 'jpg', 'JPEG',
                                 'jpeg']:  # в зависимости от типа файла выбирать метод редактирования IPTC
                    change_color_class_dng(way_to_file[0], photo_id)  # function to change IPTC data
                else:
                    change_color_class_raw(way_to_file[0],
                                           photo_id)  # function to change IPTC data

            else:

                print(f"{Fore.RED} I don't find {original_file_name} in {path}{Fore.RESET}")
                write_lost_files_info(original_file_name, photo_id)

    return file_renames  # возвращает словарь переименованных снимков


def select_folder():
    return filedialog.askdirectory()
