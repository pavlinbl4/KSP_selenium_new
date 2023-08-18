from Keyword_optimization_REFACTORING.new_input_window import input_window


def display_your_choice(what_to_do:int, keyword:str):
    green = '\33[32m'
    end = '\033[0m'

    new_keywords = None
    if what_to_do == 3:
        print(f'remove keyword {green}{keyword}{end}\n')
    elif what_to_do == 2:
        print('standard keyword optimization\n')
    elif what_to_do == 1:
        print('keyword will be deleted you sure?\n')
    elif what_to_do == 4:
        print(f'and keywords collection to images\n ')
        new_keywords = input_window()
    return new_keywords

if __name__ == '__main__':
    display_your_choice(3, "crocodile")


