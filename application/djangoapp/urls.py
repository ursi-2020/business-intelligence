from django.urls import path

from . import views


app_name = 'business-intelligence'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogue_produit', views.catalogue_produit, name='catalogue_produit'),
    path('crm', views.crm, name='crm'),
    path('get_catalogue', views.get_catalogue, name='get_catalogue'),
    path('get_crm', views.get_crm, name='get_crm')
]