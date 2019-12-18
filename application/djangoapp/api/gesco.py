import os
import json

from apipkg import api_manager as api
from datetime import datetime
from django.http import HttpResponse

from ..utils import *

from ..models import *

from django.views.decorators.csrf import csrf_exempt

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]

def get_bill(jsonLoad):
    return True
    #if not isinstance(jsonLoad["body"], dict):
    #    delivery = json.loads(jsonLoad["body"].replace("\'", "\""))
    #else:
    #    delivery = jsonLoad["body"]
    #print(jsonLoad)
    #deliv = Delivery(type=type, idCommande=delivery["idCommande"])
    #deliv.save()
    #for produit in delivery['produits']:
    #    new_produit = DeliveredProduct(codeProduit=produit['codeProduit'],
    #                                   quantite=produit['quantite'],
    #                                   delivery=deliv)
    #    new_produit.save()