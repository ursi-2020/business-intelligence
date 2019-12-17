from django.urls import path

from . import views
from .api import stock, magasin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



app_name = 'business-intelligence'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogue_produit', views.catalogue_produit, name='catalogue_produit'),
    path('crm', views.crm, name='crm'),
    path('tickets', views.tickets, name='tickets'),
    path('get_catalogue', views.get_catalogue, name='get_catalogue'),
    path('get_crm', views.get_crm, name='get_crm'),
    path('get_tickets', views.get_tickets, name='get_tickets'),
    path('delete_catalogue_produit', views.delete_catalogue_produit, name='delete_catalogue_produit'),
    path('delete_crm', views.delete_crm, name='delete_crm'),
    path('delete_tickets', views.delete_tickets, name='delete_tickets'),
    path('scheduler_crm', views.scheduler_crm, name='scheduler_crm'),
    path('scheduler_catalogue_produit', views.scheduler_catalogue_produit, name='scheduler_catalogue_produit'),
    path('scheduler_tickets', views.scheduler_tickets, name='scheduler_tickets'),
    path('tickets/data', views.get_recent_tickets_data, name='get_recent_tickets_data'),
    path('gestion-stock', views.stock, name='stock'),
    path('gestion-magasin', views.stock_magasin, name='stock_magasin'),
    path('ask_for_stock', stock.ask_for_stock, name='ask_for_stock'),
    path('ask_for_magasin_stock', magasin.ask_for_magasin_stock, name='ask_for_magasin_stock'),
    path('deliveries', views.deliveries, name='deliveries')
]

urlpatterns += staticfiles_urlpatterns()

