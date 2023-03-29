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
