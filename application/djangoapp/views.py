from django.http import HttpResponse, HttpResponseRedirect
from apipkg import api_manager as api

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *

from datetime import datetime, timedelta

import requests

from django.views.decorators.csrf import csrf_exempt

from .forms import *

import json

def index(request):
    return render(request, "index.html")

def catalogue_produit(request):
    products = Produit.objects.all()
    return render(request, "catalogue_produit.html", {'products': products})

def crm(request):
    customers = Customer.objects.all()
    return render(request, "crm.html", {'customers': customers})

def magasin(request):
    tickets = Vente.objects.all()
    for ticket in tickets:
        ticket.prix = ticket.prix / 100 
    return render(request, "magasin.html", {'tickets': tickets})    

@csrf_exempt
def get_catalogue(request):
    catalogue_request = api.send_request('catalogue-produit', 'api/get-all')
    json_data = json.loads(catalogue_request)
    for product in json_data["produits"]:
        if not Produit.objects.filter(codeProduit=product["codeProduit"]).exists():
            new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=product["prix"])
            new_product.save()
    return catalogue_produit(request)

@csrf_exempt
def get_crm(request):
    crm_request = api.send_request('crm', 'api/data')
    print(crm_request)
    json_data = json.loads(crm_request)
    print(json_data)
    for customer in json_data:
        if not Customer.objects.filter(Compte=customer['Compte']).exists():
            new_customer = Customer(Prenom=customer['Prenom'], Nom=customer['Nom'], carteFid=customer['carteFid'], Credit=customer['Credit'], Paiement=customer['Paiement'], Compte=customer['Compte'])
            new_customer.save()
    return crm(request)

@csrf_exempt
def get_tickets(request):
    magasin_request = api.send_request('gestion-magasin', 'api/sales')
    if magasin_request: 
        json_data = json.loads(magasin_request)
        for ticket in json_data:
                vente = Vente(date=ticket['date'],
                              prix=ticket['prix'],
                              client=ticket['client'],
                              pointsFidelite=ticket['pointsFidelite'],
                              modePaiement=ticket['modePaiement'])
                vente.save()
                for article_dict in ticket['articles']:
                    tmp = Produit.objects.get(codeProduit=article_dict['codeProduit'])
                    article = ArticleVendu(article=tmp,
                                           vente=vente,
                                           quantite=article_dict['quantity'])
                    article.save()
    return magasin(request)    

def delete_tickets(request):
    Vente.objects.all().delete()
    return magasin(request)

def delete_catalogue_produit(request):
    Produit.objects.all().delete()
    return catalogue_produit(request)

def delete_crm(request):
    Customer.objects.all().delete()
    return crm(request)

def scheduler_catalogue_produit(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    schedule_task('business-intelligence','get_catalogue', time, 'minute', '{}', 'business-intelligence','automatic_fetch_catalogue_produit_db')
    return catalogue_produit(request)

def scheduler_crm(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    schedule_task('business-intelligence','get_crm', time, 'minute', '{}', 'business-intelligence','automatic_fetch_crm_db')
    return crm(request)

def scheduler_tickets(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    schedule_task('business-intelligence','get_tickets', time, 'minute', '{}', 'business-intelligence','automatic_fetch_gestion-magasin_db')
    return magasin(request)        

def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text


