from variables import Keywords
import pymongo as pm
from openpyxl import load_workbook, Workbook
import os
from urllib.parse import quote_plus


# file = pd.read_excel(
#     './others/20200601_IRIT_clinicalTrials+publications.xlsx', engine='openpyxl')

# La fonction doit retourner une liste de dictionnaires avec les données de chaque ligne pour
# insérer dans une base mongoDB
def iterating_over_values(path, sheet_name):
    workbook = load_workbook(filename=path)
    if sheet_name not in workbook.sheetnames:
        print(f"'{sheet_name}' not found. Quitting.")
        return

    sheet = workbook[sheet_name]
    for value in sheet.iter_rows(
            min_col=0, max_col=11, min_row=1, max_row=402,
            values_only=False):
        l = []
        for v in value:
            if isinstance(v.value, str):
                l.append(v.value.encode("UTF-8"))
            else:
                l.append(v.value)
        print(l)


def get_maximum_rows(*, sheet_object):
    rows = 0
    for max_row, row in enumerate(sheet_object, 1):
        if not all(col.value is None for col in row):
            rows += 1
    return rows


# Génère les tests pour la fonction foundlastrow et foundlastcol


def test_foundlastrow():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(
        file_dir, 'excels', '20200601_IRIT_clinicalTrials+publications.xlsx')
    workbook = load_workbook(filename=file_path)
    sheet = workbook[Keywords.WS_CLINICALTRIALS_OBS.value]
    last = get_maximum_rows(sheet_object=sheet)
    print(last, sheet.max_column)


def __main__():
    # file_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(
    #     file_dir, 'excels', '20200601_IRIT_clinicalTrials+publications.xlsx')
    # iterating_over_values(
    #     file_path, Keywords.WS_CLINICALTRIALS_RAND.value)
    # print(db)
    test_foundlastrow()


__main__()
