from shoot_history.check_file_exist import create_file_if_not_exists
import os
import csv

def csv_writer(info, columns_name, csv_file_path):
    def write_csv_file(info, csv_file_path):
        with open(csv_file_path, 'a') as input_file:
            writer = csv.writer(input_file)
            writer.writerow(info)

    if os.path.exists(csv_file_path):
        write_csv_file(info, csv_file_path)
    else:
        info = columns_name
        write_csv_file(info, csv_file_path)


def write_lost_files_info(original_file_name, photo_id):
    csv_file = create_file_if_not_exists('Kommersant/shoot_rename', 'lost_images.csv')
    columns_name = ['original_file_name', 'photo_id']
    info = [original_file_name, photo_id]
    csv_writer(info, columns_name, csv_file)

def write_kp_files_keywords(image_id, caption, keywords):
    csv_file = create_file_if_not_exists('Kommersant', 'KR_images_keywords.csv')
    columns_name = ['image_id', 'caption', 'keywords']
    info = [image_id, caption, keywords]
    csv_writer(info, columns_name, csv_file)


if __name__ == '__main__':
    # write_lost_files_info('XXX', 'YYY')
    write_kp_files_keywords('fgfgffg', '444444444', 'fgfgfgf, 7777')