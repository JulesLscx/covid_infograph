import datetime
import json
from django.http import HttpResponse
from .files.scripttest import get_column_names, create_dic_by_sheet, get_maximum_rows, load_excel_file
from .files.variables import Keywords
from .files.connection import SingletonMongoConnection as smc


def index(request):
    l = []
    for x in smc.get_db()[Keywords.T_CLINICALTRIALS_RAND.value].findOne('NCT04362969'.encode('utf-8')):
        decode_dict = {}
        for key, value in x.items():
            if isinstance(value, bytes):
                decode_dict[key] = value.decode('utf-8')
            if isinstance(value, datetime.datetime):
                decode_dict[key] = value.strftime("%d/%m/%Y")
            else:
                decode_dict[key] = value
        l.append(decode_dict)
    return HttpResponse(json.dumps(l), content_type="application/json")
