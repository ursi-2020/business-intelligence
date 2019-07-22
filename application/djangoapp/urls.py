from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Changement par dylan --------------

    path('info/', views.test, name='test'),
    # path('info/', views.info, name='info'),

    # ------------------------------------

]