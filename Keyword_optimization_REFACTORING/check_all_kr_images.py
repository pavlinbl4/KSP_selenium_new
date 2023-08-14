from Common.authorization import autorization
from KSP_shoot_create.find_images import find_images_by_id


def main():
    # 1 autorization on site
    driver = autorization()

    # 2 find all my KR images
    find_images_by_id(shoot_id='', driver=driver)



if __name__ == '__main__':
    main()