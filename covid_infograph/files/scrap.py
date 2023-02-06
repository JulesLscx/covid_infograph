import requests
import pandas as pd
df = pd.read_csv('1 - ClinicalTrials_ObsStudies.csv')

records = []


def get_page(link):
    return requests.get(link).text


def get_doi(page):
    doi_index = page.find("doi")
    if doi_index != -1:
        return page[doi_index:].split(' ')[1]
    return None


def get_record(row):
    link = row['linkout']
    registry = row['registry']
    idd = row['id']
    try:
        page = get_page(link)
        doi = get_doi(page)
        if doi:
            return {'registry': registry, 'doi': doi}
    except:
        pass
    return None


df = pd.read_csv('1 - ClinicalTrials_ObsStudies.csv')

records = []
for index, row in df.iterrows():
    record = get_record(row)
    if record:
        records.append(record)
    print(row['registry'])

df_records = pd.DataFrame(records)
df_records.to_excel("records.xlsx", index=False)

records = []

for index, row in df.iterrows():
    link = row['linkout']
    registry = row['id']
    try:
        page = requests.get(link).text
        doi_index = page.find("doi")
        if doi_index != -1:
            doi = page[doi_index:].split(' ')[1]
            records.append({'id': registry, 'doi': doi})

        print(registry)
    except:
        pass
df_records = pd.DataFrame(records)
df_records.to_excel("records.xlsx", index=False)
