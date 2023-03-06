# use information from clip or type it manually

import pyperclip

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'


def chose_input():
    data = pyperclip.paste()
    print(f'Do you want to use {red}{data}{end}?\n'
          f'Press {green}"ENTER"{end} if {green}"YES"{end} or type you data')
    answer = input()
    return answer if len(answer) > 2 else data



