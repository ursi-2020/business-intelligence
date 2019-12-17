import os
import json

from apipkg import api_manager as api
from datetime import datetime
from django.http import HttpResponse

from ..utils import *

from ..models import *

from django.views.decorators.csrf import csrf_exempt

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]

def get_delivery(jsonLoad, type):
    body = json.loads(jsonLoad["body"].replace("\'", "\""))
    print(jsonLoad);
    for delivery in body["delivery"]:
        new_delivery = Delivery(type=type, idCommande=delivery["idCommande"])
        new_delivery.save()
        if delivery['produits'] != '':
            for produit in delivery['articles']:
                new_produit = DeliveredProduct(codeProduit=produit['codeProduit'],
                                               quantite=produit['prixAvant'],
                                               delivery=new_delivery)
                new_produit.save()


def get_stock(jsonLoad):
    body = json.loads(jsonLoad["body"].replace("\'", "\""))
    clock_time = api.send_request('scheduler', 'clock/time')
    date = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    for stock in body["stock"]:
        new_stock = Stock(date=date, codeProduit=stock["codeProduit"], quantite=stock["quantite"])
        new_stock.save()


@csrf_exempt
def ask_for_stock(request):
    sendAsyncMsg("gestion-stock", "", "get_stock")
    return HttpResponse(status=200)