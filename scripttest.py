from openpyxl import load_workbook, Workbook

# print(wb.sheetnames[2])
# print(wb.sheetnames[3])
# print(wb.sheetnames[4])

# file = pd.read_excel(
#     './others/20200601_IRIT_clinicalTrials+publications.xlsx', engine='openpyxl')


def read_all_data(path):
    workbook = load_workbook(filename=path)
    for sheet_name in workbook.sheetnames:
        if sheet_name != 'readme':
            sheet = workbook[sheet_name]
            print(f"{sheet.title=}")
            for value in sheet.iter_rows(values_only=True):
                print(value)
            break


read_all_data('./others/20200601_IRIT_clinicalTrials+publications.xlsx')
