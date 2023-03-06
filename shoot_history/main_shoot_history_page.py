from Common.authorization import autorization
from Common.choose_input import chose_input
from Common.save_page_html import save_html_page, read_html
from Common.write_xlsx import write_rename_voc
from autorization import end_selenium, open_page, work_to_history
from make_page_link import make_page_link
from _scrap_html import scrap_html, select_folder

path_to_file = '/Volumes/big4photo/Documents/Kommersant/shoot_rename/shoot_story.xlsx'

shoot_id = chose_input()

path = select_folder()

browser = autorization()

page_link = make_page_link(shoot_id)

open_page(page_link, browser)

full_history_page_source = work_to_history(browser)  # получаю данные со страницы истории

save_html_page(full_history_page_source)  # временно сохраняю страницу

file_renames = scrap_html(read_html(), path)

write_rename_voc(path_to_file, file_renames, shoot_id)

end_selenium(browser)
