import sys
import os
import json
from apipkg import api_manager
from apipkg import queue_manager as queue
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *
from application.djangoapp.api import stock, magasin


def dispatch(ch, method, properties, body):
    jsonLoad = json.loads(body)
    fromApp = jsonLoad["from"]
    functionName = ""
    if 'functionname' in jsonLoad:
        functionName = jsonLoad["functionname"]
    print(" [<] Received async from", fromApp, "with function '" + functionName + "'")

    if fromApp == 'gestion-stock':
        if functionName == 'get_stock':
            stock.get_stock(jsonLoad)
        elif functionName == 'get_delivery':
            stock.get_delivery(jsonLoad, "Livraison Magasin")
        elif functionName == 'get_resupply':
            stock.get_delivery(jsonLoad, "Commande Fournisseur")

    elif fromApp == 'gestion-magasin':
        if functionName == 'get_stock_magasin':
            magasin.get_stock_magasin(jsonLoad)

    else:
        print("Le nom de l application du json n est pas valide")

def main():
    print("Liste des ventes:")
    for v in PurchasedArticle.objects.all():
        print("ID: " + str(v.id) + "\tArticle: " + v.article.nom + "\tDate: " + str(v.date))

if __name__ == '__main__':
    queue.receive('business-intelligence', dispatch)
    main()
