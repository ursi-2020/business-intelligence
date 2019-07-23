from django.urls import path

from . import views


app_name = 'business-intelligence'

urlpatterns = [
    path('', views.index, name='index'),

    # Changement par dylan --------------

    path('test/', views.test, name='test'),
    path('hello/', views.hello, name='hello'),
    path('info/', views.info, name='info'),
    path('button/', views.button, name='button'),
    path('request/', views.request, name='request'),
    path('list/', views.list, name='list'),
    path('add-article/', views.add_article, name='add-article'),

    # ------------------------------------

]