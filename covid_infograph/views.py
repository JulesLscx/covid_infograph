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
from plotly import graph_objects as go
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


def phase_graph(request):
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value]
    dict_df = {"phase": [], "count": [], "collection": []}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate(
            [{'$group': {'_id': "$phase", 'count': {'$sum': 1}}}])
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["phase"].append(item["_id"])
            dict_df["count"].append(item["count"])
            dict_df["collection"].append(collection)
    df = pd.DataFrame(dict_df)
    df.sort_values(by=["phase", "collection"], inplace=True)
    print(df.head())
    phasegraph = px.bar(
        df,
        x="phase",
        y="count",
        color="collection",
        title="Nombre de données par phase d'étude"
    )

    phasegraph.update_layout(
        xaxis_title="Phase d'étude",
        yaxis_title="Nombre de données"
    )

    phasegraph = phasegraph.to_html(
        full_html=False,
        default_height=600, default_width=800, include_plotlyjs='cdn')
    context = {
        'phasegraph': phasegraph
    }
    return HttpResponse(render(request, 'grah_theo.html', context))


def group_by_gender_graph(request):
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value
                   ]
    dict_df = {"gender": [], "count": [], "collection": []}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate(
            [{'$group': {'_id': "$gender", 'count': {'$sum': 1}}}])
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["gender"].append(item["_id"])
            dict_df["count"].append(item["count"])
            dict_df["collection"].append(collection)
    df = pd.DataFrame(dict_df)
    genregraph = px.bar(
        df,
        x="gender",
        y="count",
        color="collection",
        title="Nombre d'essais par genre")

    genregraph.update_layout(
        xaxis_title="Genre",
        yaxis_title="Nombre d'essais"
    )
    genregraph = genregraph.to_html(
        full_html=False,
        default_height=600, default_width=800, include_plotlyjs='cdn')
    context = {
        'genregraph': genregraph
    }
    return HttpResponse(render(request, 'graph_gender.html', context))


def registry_graph(request):
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value]
    dict_df = {"registry": [], "count": [], "collection": []}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate(
            [{'$group': {'_id': "$registry", 'count': {'$sum': 1}}}])
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["registry"].append(item["_id"])
            dict_df["count"].append(item["count"])
            dict_df["collection"].append(collection)
    df = pd.DataFrame(dict_df)
    df.loc[df['count'] < 2, 'registry'] = 'autres registres'
    registrygraph = px.pie(
        df,
        values="count",
        names="registry",
        title="Nombre de données par registre")

    registrygraph = registrygraph.to_html(
        full_html=False,
        include_plotlyjs='cdn')
    context = {
        'registrygraph': registrygraph
    }
    return HttpResponse(render(request, 'graph_registry.html', context))


def Intervention_Drug_by_Date_graph(request):
    collections = [Keywords.T_CLINICALTRIALS_OBS.value,
                   Keywords.T_CLINICALTRIALS_RAND.value
                   ]
    dict_df = {"date": [], "count": [], "collection": []}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate(
            [{
                "$match": {
                    "interventions.type": "Drug"
                }
            },
                {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m", "date": "$date"}},
                    "count": {"$sum": 1}
                }
            },
                {
                "$sort": {
                    "_id": 1
                }
            }])
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["date"].append(item["_id"])
            dict_df["count"].append(item['count'])
            dict_df['collection'].append(collection)
    df = pd.DataFrame(dict_df)
    print(df.head())
    chart = px.bar(
        df,
        x='date',
        y='count',
        color='collection',
        title='Nombre d\intervention de type Drug par dates'
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
        'interventionsgraph': chart
    }
    return HttpResponse(render(request, 'graph_interventions.html', context))


def clasConcepts_graph(request):
    collections = [Keywords.T_PUBLICATION_OBS.value,
                   Keywords.T_PUBLICATION_RAND.value]
    dict_df = {"concepts": [], "count": [], "collection": []}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate(
<<<<<<< HEAD
            [{'$unwind': {'path': "$concepts",'preserveNullAndEmptyArrays': False }}, { "$group": { '_id': { 'date': { "$dateToString": {'format': '%Y-%m', 'date': "$datePublished" }}, 'concepts': "$concepts" }, 'count': { "$sum": 1 }}}, { "$sort": { 'date': 1, 'count': -1 }},{'$limit': 100 }], allowDiskUse=True)
=======
            [{'$unwind': "$concepts"}, {'$group': {'_id': "$concepts", 'count': {'$sum': 1}}}, {'$sort': {'_id': -1}}])
>>>>>>> 6bc593983f5c630b47644adfd6d32fae8031d48d
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["concepts"].append(item["_id"]['concepts'])
            dict_df["count"].append(item["count"])
            dict_df["collection"].append(collection)
    df = pd.DataFrame(dict_df)
    classement = list(range(1, 101))
    print(df.head())
<<<<<<< HEAD
    clasConceptsgraph = go.Figure(data=[go.Table(header=dict(values=['Classement', 'Concepts', 'Nombre']),
                 cells=dict(values=[classement, df['concepts'], df['count']]))
                     ])
    
    clasConceptsgraph = clasConceptsgraph.to_html(
=======
    genregraph = px.bar(
        df,
        x="date",
        y="count",
        color="collection",
        title="Nombre d'intervention de type Drug par date")

    genregraph.update_layout(
        xaxis_title="Date",
        yaxis_title="Nombre d'intervention de type Drug"
    )
    genregraph.update_layout(
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

    genregraph = genregraph.to_html(
>>>>>>> 6bc593983f5c630b47644adfd6d32fae8031d48d
        full_html=False,
        default_height=600, default_width=800, include_plotlyjs='cdn')
    context = {
        'genregraph': genregraph
    }
    return HttpResponse(render(request, 'graph_gender.html', context))
