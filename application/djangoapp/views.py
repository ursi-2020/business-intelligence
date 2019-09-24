from django.http import HttpResponse, HttpResponseRedirect
from apipkg import api_manager as api

# new import -------------------
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *

from .forms import *

import json


# -----------------------------


# def index(request):
#   time = api.send_request('scheduler', 'clock/time')
#   return HttpResponse("L'heure de la clock est %r" % time)


# Changement par dylan --------------

def test(request):
    return HttpResponse("Le test fonctionne en local")


def hello(request):
    infoB = api.send_request('gestion-stock', 'info')
    return HttpResponse("Je suis BI et tu est : %r" % infoB)


def info(request):
    return HttpResponse("Business Intelligence")


# totonio- ---- - --  -- - - --

def index(request):
    info = api.send_request('gestion-stock', 'info')
    return render(request, "index.html", {'info': info})


def request(request):
    text = api.send_request('gestion-stock', 'info')
    return HttpResponse(text)


def button(request):
    context = {}
    return render(request, "button.html", context)

def get_catalogue(request):
    catalogue_request = api.send_request('catalogue-produit', 'catalogueproduit/api/data')
    json_data = json.loads(catalogue_request)
    print(json_data)
    for product in json_data["produits"]:
        new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=product["prix"])
        new_product.save()
    return HttpResponse("Ajoute")

def print_catalogue(request):
    return

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            first = Article.objects.all().filter(nom=form['nom'].value()).first()
            if (first is None) :
                new_article = form.save()
            else :
                first.stock += int(form['stock'].value())
                first.save()
            return HttpResponseRedirect('/list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form' : form})

def list(request):
    datas = Article.objects.all()
    context = {
        'articles': datas,
    }
    return render(request, "data.html", context)

def clear(request):
    Article.objects.all().delete()
    return HttpResponseRedirect('/list')

def remove_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            first = Article.objects.all().filter(nom=form['nom'].value()).first()
            if (first is not None) :
                form_stock = int(form['stock'].value())
                if (form_stock > first.stock):
                    first.stock = 0
                else :
                    first.stock -= int(form['stock'].value())
                first.save()
            return HttpResponseRedirect('/list')
    else:
        form = ArticleForm()
    return render(request, 'remove_article.html', {'form' : form})

# ------------------------------------
