from Common.write_xlsx import write_to_file, write_xlsx_single_sheet
from published_images import publication_info, published_for_all_time

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'


def one_day_images_cycle(images_voc, i, path_to_file, count, photographer):  # # проверяю каждый снимок из "засланных"
    print(f"{red} in  {i} - {len(images_voc)} were send to publication{end}")
    for k in images_voc:  # k - внутренний id снимка
        count += 1
        used_images = publication_info(k, count, i)  # получаю словарь с данными о всех публикациях данного снимка
        write_xlsx_single_sheet(path_to_file, used_images, photographer)  # записываю данную информацию в файл отчета
    return count

