import pyexiv2
import os
from colorama import Fore
import exiftool
import logging
import pathlib

logger = logging.getLogger(__name__)


def change_color_class_raw(image_path, image_title):
    """Modify RAW image metadata using pyexiv2"""
    changes = {
        'Xmp.dc.creator': 'Eugene Pavlenko',
        'Xmp.xmp.Label': 'Red',
        'Xmp.dc.title': {'lang="x-default"': image_title}
    }
    try:
        with image_path.open('rb+') as image_file:
            with pyexiv2.ImageData(image_file.read()) as metadata:
                metadata.modify_xmp(changes)
                image_file.seek(0)
                image_file.truncate()
                image_file.write(metadata.get_bytes())
    except Exception as ex:
        logger.error("Error modifying %s: %s", image_path.name, ex)
        print(f'{Fore.RED}{ex}{Fore.RESET}in file {Fore.GREEN}{os.path.basename(file)}{Fore.RED}')


def change_color_class_dng(image_path, image_title, color):
    """Modify DNG image metadata using ExifTool"""

    try:
        with exiftool.ExifToolHelper() as et:
            et.set_tags(
                [file],
                tags={"XMP:Title": image_title,
                      'XMP:Label': color,
                      'XMP:Creator': 'Eugene Pavlenko'},
                params=["-P", "-overwrite_original"]
            )
    except Exception as ex:
        logger.error("Error modifying %s: %s", image_path.name, ex)
        print(f'{Fore.RED}{ex}{Fore.RESET}in file {Fore.GREEN}{os.path.basename(file)}{Fore.RED}')


if __name__ == '__main__':
    # file = '/Volumes/big4photo/python_test_images/20151102__PAV5906.nef'
    file = '/Volumes/big4photo/python_test_images/20230403EPAV9047.ORF'
    # file = '/Volumes/big4photo-3/2019/10_October/20191007_Недвижимость/20191007EPAV7002.ORF'
    # file = '/Volumes/big4photo/python_test_images/20230526PEV_7378.JPG'
    # file = '/Volumes/big4photo/python_test_images/20230602_PAV5801.DNG'
    # change_color_class_dng(file, 'edit_info_with_ExifToolHelper', color="Blue")

    t_image_path = pathlib.Path(file)

    change_color_class_dng(
        t_image_path,
        image_title='New title',
        color='Blue'
    )
