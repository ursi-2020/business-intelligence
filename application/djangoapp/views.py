from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

# Changement par dylan --------------

def test(request):
    return HttpResponse("Le test fonctionne en local")

def hello(request):
    infoB = api.send_request('gestion-stock', 'info')
    return HttpResponse("Je suis BI et tu est : %r" % infoB)

def info():
    return HttpResponse("Je suis BI.")

# ------------------------------------
