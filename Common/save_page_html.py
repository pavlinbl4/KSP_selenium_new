from pathlib import Path

report_folder = f'{Path.home()}/Documents/Kommersant'

def save_html_page(report_html):
    with open(f'{report_folder}/source_page.html', 'w') as file:
        file.write(report_html)


def read_html():
    with open(f'{report_folder}/source_page.html', 'r') as file:
        return file.read()