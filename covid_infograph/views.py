import datetime
from bson.json_util import dumps, loads

from django.http import HttpResponse
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc
from django.shortcuts import render
from django.template import loader


def display_data(request, page, limit=100):
    if page == 1:
        value = Keywords.T_CLINICALTRIALS_OBS.value
    elif page == 2:
        value = Keywords.T_CLINICALTRIALS_RAND.value
    elif page == 3:
        value = Keywords.T_PUBLICATION_OBS.value
    elif page == 4:
        value = Keywords.T_PUBLICATION_RAND.value
    else:
        HttpResponse("Page not found")
    if limit == 0:
        cursor = smc.get_db()[value].find()
    cursor = smc.get_db()[value].find().limit(limit)
    list_cursor = list(cursor)
    template = loader.get_template('index.html')
    context = {'data_base': dumps(list_cursor, indent=2)}
    return HttpResponse(template.render(context, request))


def accueil(request):
    template = loader.get_template('accueil.html')
    return HttpResponse(template.render(None, request))
