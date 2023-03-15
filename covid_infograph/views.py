import datetime
from bson.json_util import dumps, loads
import json
from django.http import HttpResponse
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from plotly import express as px
import pandas as pd


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
    context = {
        'page': page,
        'limit': limit,
        'date': datetime.datetime.now(),
        'titre': titre,
        'combo': dumps(combos)
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


def all_date_graph(request):
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value,
                   Keywords.T_PUBLICATION_OBS.value,
                   Keywords.T_PUBLICATION_RAND.value]
    dict_df = {"date": [], "count": [], "collection": []}
    for i, collection in enumerate(collections):
        if i < 2:
            cursor = smc.get_db()[collection].aggregate(
                [{'$group': {'_id': '$date', 'count': {'$sum': 1}}}, {'$sort': {'_id': 1}}])
        else:
            cursor = smc.get_db()[collection].aggregate(
                [{'$group': {'_id': '$datePublished', 'count': {'$sum': 1}}}, {'$sort': {'_id': 1}}])
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["date"].append(item["_id"])
            dict_df["count"].append(item["count"])
            dict_df["collection"].append(collection)
    df = pd.DataFrame(dict_df)
    print(df.head())
    chart = px.bar(
        df,
        x='date',
        y='count',
        color='collection',
        title='Nombre de données par date de publication'
    )
    chart.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    chart = chart.to_html(
        full_html=False,
        default_height=600, default_width=800, include_plotlyjs='cdn')
    context = {
        'chart': chart
    }
    return HttpResponse(render(request, 'test_chat.html', context))
