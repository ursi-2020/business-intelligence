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
    return render(request, "catalogue_produit.html", {'products': products,'products_count': Produit.objects.count()})


def crm(request):
    customers_list = Customer.objects.all()
    paginator = Paginator(customers_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    customers = paginator.get_page(page)
    fidcustomers = sum(1 for i in customers if i.Compte != "")
    return render(request, "crm.html", {'customers': customers, 'fidcustomers': fidcustomers, 'customers_count': Customer.objects.count()})


def tickets(request):
    tickets_list = Ticket.objects.all().order_by('-DateTicket')
    paginator = Paginator(tickets_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    tickets = paginator.get_page(page)

    ca = Result.objects.filter(type='CHIFFRE_AFFAIRE').last()
    if not ca:
        chiffre_affaire = 0
    else:
        chiffre_affaire = ca.value

    cout = Result.objects.filter(type='COUT').last()
    if not cout:
        benefice = 0
    else:
        benefice = chiffre_affaire - cout.value

    purchasedArticles = PurchasedArticle.objects.all()

    return render(request, "tickets.html", {'tickets': tickets, 'purchasedArticles': purchasedArticles,
                                            'chiffre_affaire': round(chiffre_affaire/100, 2), 'ticket_count': Ticket.objects.count(),
                                            'benefice': round(benefice/100, 2)})


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

def incidents(request):
    incidents_list = Incident.objects.all().order_by('-date')
    paginator = Paginator(incidents_list, 10)
    page = request.GET.get('page')
    incidents = paginator.get_page(page)
    return render(request, 'incidents.html', {'incidents': incidents, 'incidents_count': Incident.objects.count()})

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
    crm_tickets_request = api.send_request('crm', 'api/get_tickets/bi')

    ca = Result.objects.filter(type='CHIFFRE_AFFAIRE').last()
    if not ca:
        chiffre_affaire = 0
    else:
        chiffre_affaire = ca.value

    if crm_tickets_request:
        json_data = json.loads(crm_tickets_request)
        for ticket in json_data['tickets']:
            new_ticket = Ticket(DateTicket=datetime.strptime(ticket['date'], '%Y-%m-%d'), Prix=ticket['prix'],
                                Client=ticket['client'],
                                PointsFidelite=ticket['pointsFidelite'], ModePaiement=ticket['modePaiement'],
                                Promo_client=ticket['Promo_client'], Origin=ticket['origin'])
            new_ticket.save()
            chiffre_affaire += ticket['prix']
            if ticket['articles'] != '':
                for article in ticket['articles']:
                    new_article = PurchasedArticle(codeProduit=article['codeProduit'],
                                                   prixAvant=article['prixAvant'], prixApres=article['prixApres'],
                                                   promo=article['promo'], promo_client_produit=article['promo_client'],
                                                   quantity=article['quantity'], ticket=new_ticket)
                    new_article.save()
    new_ca = Result(type="CHIFFRE_AFFAIRE", value=chiffre_affaire, date=datetime.now())
    new_ca.save()
    return tickets(request)

@csrf_exempt
def get_incidents(request):
    Incident.objects.all().delete()
    gestion_paiement_incidents_request = api.send_request('gestion-paiement', 'api/incidents')

    if gestion_paiement_incidents_request:
        json_data = json.loads(gestion_paiement_incidents_request)
        for incident in json_data:
            new_incident = Incident(client_id=incident['client_id'], amount=incident['amount'], date=incident['date'])
            new_incident.save()
    return incidents(request)



def delete_tickets(request):
    PurchasedArticle.objects.all().delete()
    Ticket.objects.all().delete()
    return tickets(request)

def delete_incidents(request):
    Incident.objects.all().delete() 
    return incidents(request)   


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

def scheduler_incidents(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=180)
    schedule_task('business-intelligence', 'get_incidents', time, 'day', '{}', 'business-intelligence',
                  'automatic_fetch_gestion-magasin_db')
    return incidents(request)

def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data,
            "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers=headers, json=data)
    return r.text


def get_recent_tickets_data(request):
    eCommerce_tot = [0, 0, 0, 0, 0, 0, 0];
    eCommerce_prom = [0, 0, 0, 0, 0, 0, 0];
    eCommerce_prom_client = [0, 0, 0, 0, 0, 0, 0];
    eCommerce_prom_ticket = [0, 0, 0, 0, 0, 0, 0];
    eCommerce_classic = [0, 0, 0, 0, 0, 0, 0];

    magasin_tot = [0, 0, 0, 0, 0, 0, 0];
    magasin_prom = [0, 0, 0, 0, 0, 0, 0];
    magasin_prom_client = [0, 0, 0, 0, 0, 0, 0];
    magasin_prom_ticket = [0, 0, 0, 0, 0, 0, 0];
    magasin_classic = [0, 0, 0, 0, 0, 0, 0];

    clock_time = api.send_request('scheduler', 'clock/time')
    now = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    jours = [(now - timedelta(6)).strftime("%Y-%m-%d"),
             (now - timedelta(5)).strftime("%Y-%m-%d"),
             (now - timedelta(4)).strftime("%Y-%m-%d"),
             (now - timedelta(3)).strftime("%Y-%m-%d"),
             (now - timedelta(2)).strftime("%Y-%m-%d"),
             (now - timedelta(1)).strftime("%Y-%m-%d"),
             now.strftime("%Y-%m-%d")]

    eCommerces = PurchasedArticle.objects.filter(ticket__Origin="e-commerce")
    magasins = PurchasedArticle.objects.filter(ticket__Origin="magasin")

    for eCommerce in eCommerces:
        elapsed = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"').date() - eCommerce.ticket.DateTicket
        for i in range(7):
            if elapsed >= timedelta(days=i) and elapsed < timedelta(days=i + 1):
                if eCommerce.promo > 0:
                    eCommerce_prom[i] += 1
                if eCommerce.promo_client_produit > 0:
                    eCommerce_prom_client += 1
                if eCommerce.promo < 0 and eCommerce.promo_client_produit < 0 and eCommerce.ticket.Promo_client < 0:
                    eCommerce_classic[i] +=1
                eCommerce_tot[i] += 1
    for magasin in magasins:
        elapsed = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"').date() - magasin.ticket.DateTicket
        for i in range(7):
            if elapsed >= timedelta(days=i) and elapsed < timedelta(days=i + 1):
                if magasin.promo > 0:
                    magasin[i] += 1
                if magasin.promo_client_produit > 0:
                    magasin_prom_client += 1
                if magasin.promo < 0 and magasin.promo_client_produit < 0 and magasin.ticket.Promo_client < 0:
                    magasin_classic[i] +=1
                magasin_tot[i] += 1

    eCommerce_prom.reverse()
    eCommerce_prom_client.reverse()
    eCommerce_classic.reverse()
    eCommerce_tot.reverse()

    magasin_prom.reverse()
    magasin_prom_client.reverse()
    magasin_classic.reverse()
    magasin_tot.reverse()

    data = {
        "promotions_eCommerce": eCommerce_prom,
        "promotions_clients_eCommerce": eCommerce_prom_client,
        "classics_eCommerce": eCommerce_classic,
        "total_eCommerce": eCommerce_tot,

        "promotions_magasin": magasin_prom,
        "promotions_clients_magasin": magasin_prom_client,
        "classics_magasin": magasin_classic,
        "total_magasin": magasin_tot,
        "jours": jours
    }
    return JsonResponse(data)
