import datetime
from bson.json_util import dumps, loads

from django.http import HttpResponse
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc
from django.shortcuts import render
from django.template import loader


def index(request):
    cursor = smc.get_db()[
        Keywords.T_CLINICALTRIALS_OBS.value].find().limit(100)
    list_cursor = list(cursor)
    template = loader.get_template('page1.html')
    context = {'data_base': dumps(list_cursor, indent=2)}
    return HttpResponse(template.render(context, request))
