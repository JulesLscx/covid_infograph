from .variables import Keywords
from .connection import SingletonMongoConnection as smc


def searching(*, text: str):
    if text is None:
        return None
    if len(text) < 4:
        return None
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value,
                   Keywords.T_PUBLICATION_OBS.value,
                   Keywords.T_PUBLICATION_RAND.value]
    groupeElement = {}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate([{'$or': [
            {'title': {'$regex': text, '$options': "i"}},
            {'concept': {'$regex': text, '$options': "i"}},
            {'authors': {'$regex': text, '$options': "i"}},
            {'interventions': {'$regex': text, '$options': "i"}},
            {'abstract': {'$regex': text, '$options': "i"}}]
        }]).limit(10)
        groupeElement[collection] = list(cursor)
    return groupeElement
