from pathlib import Path
from Common.choose_input import chose_input
from Common.save_page_html import save_html_page, read_html
from Common.selenium_tools import end_selenium, open_page, work_to_history
from Common.tk_tools import select_folder_via_gui
from Common.write_xlsx import write_rename_voc
from Common.make_page_link import make_page_link
from kp_selenium_tools.authorization import AuthorizationHandler
from scrap_html import scrap_html

path_to_file = f'{Path.home()}/Documents/Kommersant/shoot_rename/shoot_story.xlsx'

# enter shoot id or use it from clipboard
shoot_id = chose_input()

path = select_folder_via_gui()

driver = AuthorizationHandler().authorize()

page_link = make_page_link(shoot_id)

open_page(page_link, driver)

full_history_page_source = work_to_history(driver)  # получаю данные со страницы истории

save_html_page(full_history_page_source)  # временно сохраняю страницу

file_renames = scrap_html(read_html(), path)  # path to folder with images

write_rename_voc(path_to_file, file_renames, shoot_id)

end_selenium(driver)
