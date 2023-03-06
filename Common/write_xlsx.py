from openpyxl import load_workbook
import string
from openpyxl.styles import Font, Color, Alignment



def write_n_rows(ws, last_line, image_info):
    alphabet = string.ascii_uppercase
    for i in range(len(image_info)):
        ws[f'{alphabet[i]}{last_line + 1}'] = image_info[alphabet[i]]


def write_to_file(path_to_file, image_info, last_line, report_date):
    wb = load_workbook(path_to_file)
    ws = wb[report_date]
    write_n_rows(ws, last_line + 1, image_info)
    wb.save(path_to_file)


def write_xlsx_single_sheet(path_to_file, image_info):
    wb = load_workbook(path_to_file)
    ws = wb.active
    last_line = ws.max_row
    write_n_rows(ws, last_line, image_info)
    wb.save(path_to_file)


def write_rename_voc(path_to_file, image_info, shoot_id):
    wb = load_workbook(path_to_file)
    ws = wb.create_sheet(shoot_id)
    ws.column_dimensions['A'].width = 50  # задаю шрину колонки
    ws.column_dimensions['B'].width = 50  # задаю шрину колонки
    ws.column_dimensions['C'].width = 40  # задаю шрину колонки
    ws.cell(row=1, column=1).value = "KSP name"
    ws.cell(row=1, column=2).value = "original file name"
    ws.cell(row=1, column=3).value = "published"
    last_line = ws.max_row
    for k in image_info:
        last_line += 1
        ws.cell(row=last_line, column=1).value = k
        ws.cell(row=last_line, column=2).value = image_info[k][0]
        if len(image_info[k]) == 2:
            ws.cell(row=last_line, column=3).value = image_info[k][1]
            ws.cell(row=last_line, column=1).font = Font(color="FF0000")
            ws.cell(row=last_line, column=2).font = Font(color="FF0000")
            ws.cell(row=last_line, column=3).font = Font(color="FF0000")
    wb.save(path_to_file)
            
            





