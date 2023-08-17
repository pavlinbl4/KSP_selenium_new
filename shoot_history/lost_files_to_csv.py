from shoot_history.check_file_exist import create_file_if_not_exists
from shoot_history.csv_writer import csv_writer


def write_lost_files_info(original_file_name, photo_id):
    csv_file = create_file_if_not_exists('Kommersant/shoot_rename', 'lost_images.csv')
    columns_name = ['original_file_name', 'photo_id']
    info = [original_file_name, photo_id]
    csv_writer(info, columns_name, csv_file)

def write_kp_files_keywords(image_id, caption, keywords):
    csv_file = create_file_if_not_exists('Kommersant', 'images_keywords.csv')
    columns_name = ['image_id', 'caption', 'keywords']
    info = [image_id, caption, keywords]
    csv_writer(info, columns_name, csv_file)


if __name__ == '__main__':
    # write_lost_files_info('XXX', 'YYY')
    write_kp_files_keywords('fgfgffg', '444444444', 'fgfgfgf, 7777')