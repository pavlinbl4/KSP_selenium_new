import exiftool


def change_color_class(file, image_title, color):
    with exiftool.ExifToolHelper() as et:
        et.set_tags(
            [file],
            tags={"XMP:Title": image_title,
                  'XMP:Label': color,
                  'XMP:Creator': 'Eugene Pavlenko'},
            params=["-P", "-overwrite_original"]
        )

if __name__ == '__main__':
    file = '/Volumes/big4photo/python_test_images/20151102__PAV5906.nef'
    change_color_class(file, 'image_title', color='Red"')
