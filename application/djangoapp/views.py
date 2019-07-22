from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

# Changement par dylan --------------

def test(request):
    message = api.send_request('apptest', '/infoBTest')
    return HttpResponse("Le message de l'application partenaire est : %r" % message)

#def info(request):
   # return HttpResponse("Je suis BI.")

# ------------------------------------
