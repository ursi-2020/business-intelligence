from django.http import HttpResponse, HttpResponseRedirect
from apipkg import api_manager as api

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *

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


def get_catalogue(request):
    catalogue_request = api.send_request('catalogue-produit', 'api/data')
    json_data = json.loads(catalogue_request)
    for product in json_data["produits"]:
        if not Produit.objects.filter(codeProduit=product["codeProduit"]).exists():
            new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=product["prix"])
            new_product.save()
    return catalogue_produit(request)

def get_crm(request):
    crm_request = api.send_request('crm', 'api/data')
    print(crm_request)
    json_data = json.loads(crm_request)
    print(json_data)
    for customer in json_data:
        if not Customer.objects.filter(account=customer['account']).exists():
            new_customer = Customer(firstName=customer['firstName'], lastName=customer['lastName'], fidelityPoint=customer['fidelityPoint'], payment=customer['payment'], account=customer['account'])
            new_customer.save()
    return crm(request)

