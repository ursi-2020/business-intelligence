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
    if not isinstance(jsonLoad["body"], dict):
        bill = json.loads(jsonLoad["body"].replace("\'", "\""))
    else:
        bill = jsonLoad["body"]
    print(jsonLoad)

    c = Result.objects.filter(type='COUT').last()
    if not c:
        cout = 0
    else:
        cout = c.value

    for factures in bill['factures']:
        f = Facture(numeroFacture=factures["numeroFacture"],
                       dateFacture=datetime.strptime(factures["dateFacture"], '%Y-%m-%d'),
                       datePaiement=datetime.strptime(factures["datePaiement"], '%Y-%m-%d'),
                       numeroCommande=factures["numeroCommande"],
                       dateLivraison=datetime.strptime(factures["dateLivraison"], '%Y-%m-%d')
                    )
        f.save()
        for item in factures['items']:
            factureItem = FactureItem(codeProduit=item['codeProduit'], prix=item['prix'], quantite=item['quantite'], facture=f)
            factureItem.save()
            cout += item['prix'] * item['quantite']

    new_cout = Result(type="COUT", value=cout, date=datetime.now())
    new_cout.save()