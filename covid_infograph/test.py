import datetime
from bson.json_util import dumps, loads

from django.http import HttpResponse
from .files.scripttest import get_column_names, create_dic_by_sheet, get_maximum_rows, load_excel_file
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc


def index(request):
    cursor = smc.get_db()[Keywords.T_CLINICALTRIALS_OBS.value].find()
    list_cursor = list(cursor)
    json_data = dumps(list_cursor, indent=2)
    return HttpResponse(json_data, content_type='application/json')
