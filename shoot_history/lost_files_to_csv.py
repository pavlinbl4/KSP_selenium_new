from check_file_exist import create_file_if_no
from csv_writer import csv_writer


def write_lost_files_info(original_file_name, photo_id):
    csv_file = create_file_if_no('/Volumes/big4photo/Documents/Kommersant/shoot_rename', 'lost_images.csv')
    columns_name = ['original_file_name', 'photo_id']
    info = [original_file_name, photo_id]
    csv_writer(info, columns_name, csv_file)


if __name__ == '__main__':
    print(write_lost_files_info('20220622PEV_4551', 'KSP_017605_00008'))
