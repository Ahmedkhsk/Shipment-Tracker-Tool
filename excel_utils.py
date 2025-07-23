import openpyxl

def update_excel(excel_file, bl_number, eta):
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
    headers = {cell.value: idx for idx, cell in enumerate(next(sheet.iter_rows(min_row=1, max_row=1)))}
    row = ["" for _ in range(len(headers))]
    if "رقم الحاوية" in headers:
        row[headers["رقم الحاوية"]] = bl_number
    if "تاريخ الوصول" in headers:
        row[headers["تاريخ الوصول"]] = eta
    sheet.append(row)
    workbook.save(excel_file)
    print("Excel updated successfully.")