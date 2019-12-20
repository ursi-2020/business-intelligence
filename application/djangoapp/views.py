from django.http import HttpResponse, HttpResponseRedirect
from apipkg import api_manager as api

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *

from datetime import datetime, timedelta

import requests

from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .forms import *

import json


def index(request):
    return render(request, "index.html")


def catalogue_produit(request):
    products_list = Produit.objects.all()
    paginator = Paginator(products_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, "catalogue_produit.html", {'products': products})


def crm(request):
    customers_list = Customer.objects.all()
    paginator = Paginator(customers_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    customers = paginator.get_page(page)
    fidcustomers = sum(1 for i in customers if i.Compte != "")
    return render(request, "crm.html", {'customers': customers, 'fidcustomers': fidcustomers})


def tickets(request):
    tickets_list = Ticket.objects.all()
    paginator = Paginator(tickets_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    tickets = paginator.get_page(page)

    chiffre_affaire = 0
    for ticket in tickets:
        ticket.Prix = ticket.Prix / 100
        chiffre_affaire = chiffre_affaire + ticket.Prix
    purchasedArticles = PurchasedArticle.objects.all()

    return render(request, "tickets.html", {'tickets': tickets, 'purchasedArticles': purchasedArticles,
                                            'chiffre_affaire': round(chiffre_affaire, 2)})


def stock(request):
    #clock_time = api.send_request('scheduler', 'clock/time')
    #now = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    #stocks = Stock.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day)
    stocks_list = Stock.objects.all().order_by('-date')
    paginator = Paginator(stocks_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    return render(request, "stock.html", {'stocks': stocks})


def stock_magasin(request):
    #clock_time = api.send_request('scheduler', 'clock/time')
    #now = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    #stocks = StockMagasin.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day)
    stocks_list = StockMagasin.objects.all().order_by('-date')
    paginator = Paginator(stocks_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    return render(request, "stock_magasin.html", {'stocks': stocks})

def deliveries(request):
    deliveries_list = Delivery.objects.all()
    deliveredProducts = DeliveredProduct.objects.all()
    paginator = Paginator(deliveries_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    deliveries = paginator.get_page(page)
    return render(request, "bon_livraison.html", {'deliveries': deliveries, 'deliveredProducts': deliveredProducts})


@csrf_exempt
def get_catalogue(request):
    catalogue_request = api.send_request('catalogue-produit', 'api/get-all')
    json_data = json.loads(catalogue_request)
    for product in json_data["produits"]:
        if not Produit.objects.filter(codeProduit=product["codeProduit"]).exists():
            new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"],
                                  descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"],
                                  packaging=product["packaging"], prix=product["prix"])
            new_product.save()
    return catalogue_produit(request)


@csrf_exempt
def get_crm(request):
    crm_request = api.send_request('crm', 'api/data')
    json_data = json.loads(crm_request)
    for customer in json_data:
        if not Customer.objects.filter(Compte=customer['Compte']).exists():
            new_customer = Customer(Prenom=customer['Prenom'], Nom=customer['Nom'], carteFid=customer['IdClient'],
                                    Credit=customer['Credit'], Montant=customer['Montant'], Compte=customer['Compte'])
            new_customer.save()
    return crm(request)


@csrf_exempt
def get_tickets(request):
    crm_tickets_request = api.send_request('crm', 'api/get_tickets')
    if crm_tickets_request:
        json_data = json.loads(crm_tickets_request)
        for ticket in json_data['tickets']:
            new_ticket = Ticket(DateTicket=datetime.strptime(ticket['date'], '%Y-%m-%d'), Prix=ticket['prix'],
                                Client=ticket['client'],
                                PointsFidelite=ticket['pointsFidelite'], ModePaiement=ticket['modePaiement'])
            new_ticket.save()
            if ticket['articles'] != '':
                for article in ticket['articles']:
                    new_article = PurchasedArticle(codeProduit=article['codeProduit'],
                                                   prixAvant=article['prixAvant'], prixApres=article['prixApres'],
                                                   promo=article['promo'], quantity=article['quantity'],
                                                   ticket=new_ticket)
                    new_article.save()
    return tickets(request)


def delete_tickets(request):
    PurchasedArticle.objects.all().delete()
    Ticket.objects.all().delete()
    return tickets(request)


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
    schedule_task('business-intelligence', 'get_catalogue', time, 'minute', '{}', 'business-intelligence',
                  'automatic_fetch_catalogue_produit_db')
    return catalogue_produit(request)


def scheduler_crm(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    schedule_task('business-intelligence', 'get_crm', time, 'minute', '{}', 'business-intelligence',
                  'automatic_fetch_crm_db')
    return crm(request)


def scheduler_tickets(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=180)
    schedule_task('business-intelligence', 'get_tickets', time, 'day', '{}', 'business-intelligence',
                  'automatic_fetch_gestion-magasin_db')
    return magasin(request)


def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data,
            "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers=headers, json=data)
    return r.text


def get_recent_tickets_data(request):
    nb_tot = [0, 0, 0, 0, 0, 0, 0];
    nb_prom = [0, 0, 0, 0, 0, 0, 0];
    nb_classic = [0, 0, 0, 0, 0, 0, 0];
    clock_time = api.send_request('scheduler', 'clock/time')
    now = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    jours = [(now - timedelta(6)).strftime("%Y-%m-%d"),
             (now - timedelta(5)).strftime("%Y-%m-%d"),
             (now - timedelta(4)).strftime("%Y-%m-%d"),
             (now - timedelta(3)).strftime("%Y-%m-%d"),
             (now - timedelta(2)).strftime("%Y-%m-%d"),
             (now - timedelta(1)).strftime("%Y-%m-%d"),
             now.strftime("%Y-%m-%d")]

    promotions = PurchasedArticle.objects.exclude(promo=0)
    classics = PurchasedArticle.objects.filter(promo=0)

    for prom in promotions:
        elapsed = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"').date() - prom.ticket.DateTicket
        for i in range(7):
            if elapsed >= timedelta(days=i) and elapsed < timedelta(days=i + 1):
                nb_prom[i] += 1
    for classic in classics:
        elapsed = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"').date() - classic.ticket.DateTicket
        for i in range(7):
            if elapsed >= timedelta(days=i) and elapsed < timedelta(days=i + 1):
                nb_classic[i] += 1

    for i in range(7):
        nb_tot[i] = nb_prom[i] + nb_classic[i]

    nb_prom.reverse()
    nb_classic.reverse()
    nb_tot.reverse()

    data = {
        "promotions": nb_prom,
        "classics": nb_classic,
        "total": nb_tot,
        "jours": jours
    }
    return JsonResponse(data)
