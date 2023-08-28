import exiftool


def write_data_to_photo_iptc_tools(file):
    with exiftool.ExifToolHelper() as et:
        title = "exiftool"
        et.set_tags(
            [file],
            tags={"XMP:Title": title,
                  "IPTC:ObjectName": title,
                  'XMP:Label': "Green",
                  'XMP:Subject': "keywords/exiftool",
                  'XMP:Description': "caption/exiftool",
                  'XMP:Rating': "3",
                  'XMP:Creator': 'Eugene Pavlenko/exiftool'},
            params=["-P", "-overwrite_original"]
        )
