import os

from django.apps import AppConfig
from apipkg import api_manager as api
from datetime import datetime, timedelta

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]


def schedule_tickets(time):
    target_app = 'business-intelligence'
    target_url = 'get_tickets'
    data = '{}'
    source_app = "business-intelligence"
    name = "BI : Fetch Tickets"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_magasin_stock(time):
    target_app = 'business-intelligence'
    target_url = 'ask_for_magasin_stock'
    data = '{}'
    source_app = "business-intelligence"
    name = "BI : Ask for Magasin Stock"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_entrepot_stock(time):
    target_app = 'business-intelligence'
    target_url = 'ask_for_stock'
    data = '{}'
    source_app = "business-intelligence"
    name = "BI : Ask for Stock"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_client(time):
    target_app = 'business-intelligence'
    target_url = 'get_crm'
    data = '{}'
    source_app = "business-intelligence"
    name = "BI : Get Clients"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_catalogue(time):
    target_app = 'business-intelligence'
    target_url = 'get_catalogue'
    data = '{}'
    source_app = "business-intelligence"
    name = "BI : Get Catalogue"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_incident(time):
    target_app = 'business-intelligence'
    target_url = 'get_incidents'
    data = '{}'
    source_app = "business-intelligence"
    name = "BI : Get Incident"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            api.unregister(os.environ['DJANGO_APP_NAME'])
            api.register(myappurl, os.environ['DJANGO_APP_NAME'])

            clock_time = api.send_request('scheduler', 'clock/time')
            time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
            time = time + timedelta(seconds=180)
            schedule_client(time)
            schedule_catalogue(time)
            schedule_tickets(time)
            schedule_magasin_stock(time)
            schedule_entrepot_stock(time)
            schedule_incident(time)
