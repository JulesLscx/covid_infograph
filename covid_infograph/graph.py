from covid_infograph.forms import DateForm
from plotly import graph_objects as go
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc
from plotly import express as px
import pandas as pd
import datetime


def numberOfDataByPublicationDate():
    # First graph - number of data by publication date
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
            if item["_id"] is None or not isinstance(item["_id"], datetime.datetime):
                continue
            dict_df["date"].append(item["_id"])
            dict_df["count"].append(item["count"])
            dict_df["collection"].append(collection)
    df = pd.DataFrame(dict_df)
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby([pd.Grouper(key='date', freq='M'),
                    'collection']).sum().reset_index()
    chart = px.bar(
        df,
        x='date',
        y='count',
        color='collection',
        title='Nombre de données par date de publication'
    )
    end_date = "2020-12-31"
    start_date = "2020-01-01"
    chart.update_xaxes(type="date", range=[start_date, end_date])
    min_date = df['date'].min()
    max_date = df['date'].max()
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
    chart_div = chart.to_html(
        full_html=False,
        default_height=600, default_width=700, include_plotlyjs='cdn')
    return chart_div


def registery_graph():
    # Second graph - number of data by registry
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
    registrygraph_div = registrygraph.to_html(
        full_html=False,
        default_height=600, default_width=700, include_plotlyjs='cdn')
    return registrygraph_div


def clasConcepts_graph(request):

    month = request.GET.get('month')

    if month is None:
        request = [{'$unwind': {'path': "$concepts", 'preserveNullAndEmptyArrays': False}}, {"$group": {'_id': {
            'concepts': "$concepts"}, 'count': {"$sum": 1}}}, {"$sort": {'count': -1}}, {'$limit': 100}]
    else:
        request = [{'$unwind': {'path': "$concepts", 'preserveNullAndEmptyArrays': False}}, {"$group": {'_id': {'date': {"$dateToString": {'format': '%m-%Y',
                                                                                                                                           'date': "$datePublished"}}, 'concepts': "$concepts"}, 'count': {"$sum": 1}}}, {'$match': {'_id.date': month}}, {"$sort": {'date': 1, 'count': -1}}, {'$limit': 100}]
    collections = [Keywords.T_PUBLICATION_OBS.value,
                   Keywords.T_PUBLICATION_RAND.value]
    dict_df = {"concepts": [], "count": []}
    for i, collection in enumerate(collections):
        cursor = smc.get_db()[collection].aggregate(
            request, allowDiskUse=True)
        list_cursor = list(cursor)
        for item in list_cursor:
            dict_df["concepts"].append(item["_id"]['concepts'])
            dict_df["count"].append(item["count"])
    df = pd.DataFrame(dict_df)
    df = df.groupby(['concepts'], as_index=False).sum(numeric_only=True).sort_values(
        by=['count'], ascending=False)
    clasConceptsgraph = go.Figure(data=[go.Table(header=dict(values=['Concepts', 'Nombre']),
                                                 cells=dict(values=[df['concepts'], df['count']]))
                                        ])

    clasConceptsgraph = clasConceptsgraph.to_html(
        full_html=False,
        include_plotlyjs='cdn')
    context = {
        'clasConceptsgraph': clasConceptsgraph,
        'form': DateForm()}
    return context
