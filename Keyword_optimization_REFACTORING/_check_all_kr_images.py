
from Common.selenium_tools import number_of_founded_images, images_rotator, end_selenium, \
    find_all_images_on_site_by_shoot_id_or_keyword
from kp_selenium_tools.authorization import AuthorizationHandler


def main():
    # 1 authorization on site
    driver = AuthorizationHandler().authorize()

    # 2 find all my KR images
    find_all_images_on_site_by_shoot_id_or_keyword(shoot_id='', driver=driver, only_kr=True)

    # 3 take number of images from site
    keyword_link, images_number = number_of_founded_images(keyword='', driver=driver)

    # 4 check all find images
    images_rotator(images_number, keyword_link, driver)

    # 5 work complete close driver
    end_selenium(driver)


if __name__ == '__main__':
    main()
