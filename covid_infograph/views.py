import datetime
from bson.json_util import dumps, loads
import json
from django.http import HttpResponse
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


def find_all(request, page, limit=100):
    if page == 1:
        value = Keywords.T_CLINICALTRIALS_OBS.value
    elif page == 2:
        value = Keywords.T_CLINICALTRIALS_RAND.value
    elif page == 3:
        value = Keywords.T_PUBLICATION_OBS.value
    elif page == 4:
        value = Keywords.T_PUBLICATION_RAND.value
    else:
        HttpResponse(
            "Page not found, please check the url check the documentation")
    if limit == 0:
        cursor = smc.get_db()[value].find()
    cursor = smc.get_db()[value].find().limit(limit)
    list_cursor = list(cursor)
    return HttpResponse(dumps(list_cursor))


def display_data(request, page, limit=100):
    if page not in range(1, 5):
        return HttpResponse("Page not found")
    if page == 1:
        titre = Keywords.WS_CLINICALTRIALS_OBS.value
        combos = {}
        combos['registery'] = smc.get_db(
        )[Keywords.T_CLINICALTRIALS_OBS.value].distinct('registery')
        combos['phase'] = smc.get_db(
        )[Keywords.T_CLINICALTRIALS_OBS.value].distinct('phase')
    elif page == 2:
        titre = Keywords.WS_CLINICALTRIALS_RAND.value
        combos = {}
        combos['registery'] = smc.get_db(
        )[Keywords.T_CLINICALTRIALS_RAND.value].distinct('registery')
        combos['phase'] = smc.get_db(
        )[Keywords.T_CLINICALTRIALS_RAND.value].distinct('phase')
    elif page == 3:
        titre = Keywords.WS_PUBLICATION_OBS.value
        combos = {}
        combos['publisher'] = smc.get_db(
        )[Keywords.T_PUBLICATION_OBS.value].distinct('publisher')
        combos['venue'] = smc.get_db(
        )[Keywords.T_PUBLICATION_OBS.value].distinct('venue')
        combos['concepts'] = smc.get_db(
        )[Keywords.T_PUBLICATION_OBS.value].aggregate([{'$unwind': '$concepts'}, {'$group': {'_id': '$concepts'}}])
    elif page == 4:
        titre = Keywords.WS_PUBLICATION_RAND.value
    for key in combos:
        combos[key] = dumps(combos[key])
    context = {
        'page': page,
        'limit': limit,
        'date': datetime.datetime.now(),
        'titre': titre,
        'combos': combos
    }
    return HttpResponse(render(request, 'index.html', context))


@csrf_exempt
def display_data_filter(request, page, limit=100):
    if page == 1:
        value = Keywords.T_CLINICALTRIALS_OBS.value
    elif page == 2:
        value = Keywords.T_CLINICALTRIALS_RAND.value
    elif page == 3:
        value = Keywords.T_PUBLICATION_OBS.value
    elif page == 4:
        value = Keywords.T_PUBLICATION_RAND.value
    else:
        return HttpResponse(
            "Page not found, please check the url check the documentation")
    if request.method != 'POST':
        return HttpResponse("Error, shsould be a POST request")
    data_dict = json.loads(request.body.decode('utf-8'))
    filters = filter_builder(data_dict)
    cursor = smc.get_db()[value].aggregate(filters)
    return HttpResponse(dumps(list(cursor)))


def display_graph(request, page, limit=100):
    if page == 1:
        value = Keywords.T_CLINICALTRIALS_OBS.value
    elif page == 2:
        value = Keywords.T_CLINICALTRIALS_RAND.value
    elif page == 3:
        value = Keywords.T_PUBLICATION_OBS.value
    elif page == 4:
        value = Keywords.T_PUBLICATION_RAND.value
    else:
        return HttpResponse(
            "Page not found, please check the url check the documentation")
    cursor = smc.get_db()[value].find({'date': 1})
    list_cursor = list(cursor)
    return HttpResponse(render(request, 'graph.html', {'dates': list_cursor, 'page': page}))


def filter_builder(filters):
    filters = []
    return filters


def accueil(request):
    template = loader.get_template('accueil.html')
    return HttpResponse(template.render(None, request))
