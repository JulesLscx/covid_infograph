from variables import Keywords
from openpyxl import load_workbook, Workbook
import os
import sys


# file = pd.read_excel(
#     './others/20200601_IRIT_clinicalTrials+publications.xlsx', engine='openpyxl')


def iterating_over_values(path, sheet_name):
    workbook = load_workbook(filename=path)
    if sheet_name not in workbook.sheetnames:
        print(f"'{sheet_name}' not found. Quitting.")
        return

    sheet = workbook[sheet_name]
    for value in sheet.iter_rows(
            min_col=0, max_col=11, min_row=1, max_row=402,
            values_only=False):
        print(value[0].value)


iterating_over_values(
    './others/20200601_IRIT_clinicalTrials+publications.xlsx', Keywords.WS_CLINICALTRIALS_OBS)
