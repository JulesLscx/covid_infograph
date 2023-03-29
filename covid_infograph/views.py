import datetime
import os
from bson.json_util import dumps, loads
import json
from django.http import HttpResponse
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from plotly import express as px
from plotly import graph_objects as go
import pandas as pd
from django import forms
from .forms import DateForm
from .graph import *
from django.http import JsonResponse


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
        tmp = smc.get_db(
        )[Keywords.T_PUBLICATION_OBS.value].distinct('publisher')
        dic = {}
        for item in tmp:
            dic[item] = item
        combos['publisher'] = dic
        dic = {}
        tmp = smc.get_db(
        )[Keywords.T_PUBLICATION_OBS.value].distinct('venue')
        for item in tmp:
            dic[item] = item
        combos['venue'] = dic
    elif page == 4:
        titre = Keywords.WS_PUBLICATION_RAND.value
        combos = {}
        tmp = smc.get_db(
        )[Keywords.T_PUBLICATION_RAND.value].distinct('publisher')
        dic = {}
        for item in tmp:
            dic[item] = item
        combos['publisher'] = dic
        dic = {}
        tmp = smc.get_db(
        )[Keywords.T_PUBLICATION_RAND.value].distinct('venue')
        for item in tmp:
            dic[item] = item
        combos['venue'] = dic
    context = {
        'page': page,
        'limit': limit,
        'date': datetime.datetime.now(),
        'titre': titre,
        'combo': dumps(combos)
    }
    return HttpResponse(render(request, 'index.html', context))


def accueil(request):
    chart_div = numberOfDataByPublicationDate()
    registrygraph_div = registery_graph()
    tmp = clasConcepts_graph(request)
    concept_table = tmp['clasConceptsgraph']
    venueChart = clasVenue_month(request)
    gender_graph = group_by_gender_graph()
    intervention_drug = Intervention_Drug_by_Date_graph()
    phase = phase_graph()
    # Render the dashboard with the two graphs
    context = {
        'chart_div': chart_div,
        'registrygraph_div': registrygraph_div,
        'clasConceptsgraph': concept_table,
        'form': tmp['form'],
        'chartVenue': venueChart,
        'gender': gender_graph,
        'intervention_drug': intervention_drug,
        'phase': phase
    }
    return render(request, 'dashboard.html', context)


def upload_file(request):
    from .forms import UploadFileForm
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    _path = os.path.join('/covid_infograph/files/excels/', f.name)
    with open(_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def rechercheText(request, text):
    collections = [
        Keywords.T_CLINICALTRIALS_OBS.value,
        Keywords.T_CLINICALTRIALS_RAND.value,
        Keywords.T_PUBLICATION_OBS.value,
        Keywords.T_PUBLICATION_RAND.value
    ]
    groupeElement = []
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate([
            {
                "$match": {
                    "title": {
                        "$regex": text,
                        "$options": "i"
                    }}
            },
            {
                "$limit": 100
            }
        ])
        list_cursor = list(cursor)
        groupeElement += list_cursor
    return JsonResponse(groupeElement, safe=False)


def recherchePage(request):
    return render(request, 'recherche.html')


def readme(request):
    return render(request, 'more_about.html')
