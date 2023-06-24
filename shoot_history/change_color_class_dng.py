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
    file = '/Users/evgeniy/Pictures/2023/20230613_Брега - мегалит/20230613EPAV7980.DNG'
    change_color_class(file, 'image_title', color='Blue')
