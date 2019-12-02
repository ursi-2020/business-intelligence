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
    name = "BI-fetch-tickets"
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
            schedule_tickets(time)

