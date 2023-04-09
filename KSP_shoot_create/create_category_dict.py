import re


def read_html():
    category_dict = {}
    with open('category.txt', 'r') as text_file:
        all_lines = text_file.readlines()
        for line in all_lines:
            line = line.strip()
            category_dict[re.search(r'(?<=>).*(?=<)', line).group(0)] = re.search(r'\d+', line).group(0)
        return category_dict


if __name__ == '__main__':
    print(read_html())
