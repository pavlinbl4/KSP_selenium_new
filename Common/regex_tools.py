import re


def make_text_edit_link(link):
    inner_id = re.findall(r'(?<=id=)\d+', link)[0]
    image_id = re.findall(r'(?<=photocode=)[^&]+', link)[0]
    # image_edit_link = f'https://image.kommersant.ru/photo/archive/ViewPhoto.asp?ID={inner_id}&Lang=1&L=1'
    image_edit_link = f'https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID={inner_id}&CloseForm=1'
    return image_edit_link, image_id, inner_id
