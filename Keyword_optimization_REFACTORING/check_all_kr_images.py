from Common.authorization import autorization
from KSP_shoot_create.find_images import find_images_by_id
from Common.selenium_tools import check_keywords_number, images_rotator


def main():
    # 1 autorization on site
    driver = autorization()

    # 2 find all my KR images
    find_images_by_id(shoot_id='', driver=driver)

    # 3 take number of images from site
    keyword_link, images_number = check_keywords_number(keyword='', driver=driver)

    # 4 check all find images
    images_rotator(images_number, keyword_link, driver)

    # 5 work complite close driver


if __name__ == '__main__':
    main()
