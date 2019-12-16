from django.shortcuts import render, redirect
import json
from .models import *
from apipkg import api_manager
from apipkg import queue_manager as queue
import os


# Fonctions utiles

def sendAsyncMsg(to, body, functionName):
    time = api_manager.send_request('scheduler', 'clock/time')
    print(" [>] Sending Async message to", to, "with function", functionName)
    message = '{ "from":"' + os.environ[
        'DJANGO_APP_NAME'] + '", "to": "' + to + '", "datetime": ' + time + ', "body": ' + json.dumps(
        body) + ', "functionname":"' + functionName + '"}'
    queue.send(to, message)
