from xlutils.copy import copy
import xlrd

path = r'D:\resource_AI\THE DETECTION OF CIRCLE\测试记录.xls'
excel_data = xlrd.open_workbook(path)
sheet = excel_data.sheet_by_index(0)
row_all = sheet.nrows
col_all = sheet.ncols
print(row_all, col_all)


def save_excel(row, col, value, path):
    rb = xlrd.open_workbook(path)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row, col, value)
    wb.save(path)

# save_excel(1, 5, '11111111111', r'D:\resource_AI\THE DETECTION OF CIRCLE\test.xls')
