import requests
import pandas as pd
from variables import Keywords
from connection import SingletonMongoConnection as smc
from bs4 import BeautifulSoup


def get_documents_without_authors(*, collection, registry) -> list[dict]:
    result = smc.get_db()[collection].find(
        {'registry': registry}, {'registry': 1, 'linkout': 1})
    list_cursor = list(result)
    return list_cursor


def find_authors_clinical_gov():
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value]
    for collection in collections:
        result = get_documents_without_authors(
            registry='ClinicalTrials.gov', collection=collection)
        print(result)
        for item in result:
            url = item['linkout']
            a = requests.get(url)
            soup = BeautifulSoup(a.text, 'html.parser')
            authors = []
            for contact in soup.find_all(attrs={"headers": "contactName"}):
                txt = contact.text.replace('Contact: ', '')
                authors.append(txt)
            for contact in soup.find_all(attrs={"headers": "name"}):
                authors.append(contact.text.replace('Contact: ', ''))
            smc.get_db()[collection].update_one(
                {'_id': item['_id']}, {'$set': {'authors': authors}})



