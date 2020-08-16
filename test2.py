from openpyxl import load_workbook
excel = load_workbook('50_did.xlsx')
table = excel.get_sheet_by_name('sheet1')
for cell in table['c']:
    print(cell)