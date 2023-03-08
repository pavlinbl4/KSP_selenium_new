import re
import pyperclip
from colorama import Fore


def control_id(photo_id):
    pattern = r'\A(KSP|KMO)_\d{6,}\Z'
    if re.match(pattern, photo_id):
        photo_id = photo_id
        print(f'{photo_id = }')
        return photo_id
    print(f'{Fore.RED}not correct input\n{Fore.RESET}{Fore.GREEN}Please type photo id\n{Fore.RESET}')
    photo_id = input()
    return control_id(photo_id)


if __name__ == '__main__':
    control_id('KSP')
