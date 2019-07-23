from django.http import HttpResponse, HttpResponseRedirect
from apipkg import api_manager as api

# new import -------------------
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *

from .forms import *


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
    return HttpResponse("Je suis BI.r")


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



def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            first = Article.objects.all().filter(nom=form['nom'].value()).first()
            if (first is None):
                new_article = form.save()
            else:
                first.stock += int(form['stock'].value())
                first.save()
            return HttpResponseRedirect('/')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})


def list(request):
    datas = Article.objects.all()
    context = {
        'articles': datas,
    }
    return render(request, "data.html", context)

# ------------------------------------
