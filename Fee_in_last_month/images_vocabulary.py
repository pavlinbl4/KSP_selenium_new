import re


def make_image_dict(image_links: list[str]) -> dict[str, str]:
    image_dict = {}
    for i in image_links:
        # Extract KSP ID from image link
        ksp_id = re.findall(r'(?<=photocode=)\w{16}', str(i))[0]
        # Extract photoid from image link
        regex = r'(?<=photoid=)\d{5,7}(?=\")'
        try:
            photoid = re.findall(regex, str(i))[0]
        except IndexError:
            print(str(i))
        else:
            image_dict[photoid] = ksp_id

    return image_dict


