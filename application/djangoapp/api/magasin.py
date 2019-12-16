import os
import json

from apipkg import api_manager as api
from datetime import datetime
from django.http import HttpResponse

from ..utils import *

from ..models import *

from django.views.decorators.csrf import csrf_exempt

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]


def get_stock_magasin(jsonLoad):
    print(jsonLoad)
    body = json.loads(jsonLoad["body"].replace("\'", "\""))
    clock_time = api.send_request('scheduler', 'clock/time')
    date = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    print(body)
    for stock in body["stock"]:
        new_stock = StockMagasin(date=date, codeProduit=stock["codeProduit"], numeroFournisseur=stock["numeroFournisseur"],
                                 codeFournisseur=stock["codeFournisseur"], stockDisponible=stock["stockDisponible"])
        new_stock.save()

@csrf_exempt
def ask_for_magasin_stock(request):
    sendAsyncMsg("gestion-magasin", "", "ask_for_stock")
    return HttpResponse(status=200)