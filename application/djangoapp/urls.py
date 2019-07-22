from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Changement par dylan --------------

    path('test/', views.test, name='test'),
    path('info/', views.hellogestionstock(), name='hellogestionstock'),

    # ------------------------------------

]