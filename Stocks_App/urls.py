from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('query_results', views.query_results, name='query_results'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('index', views.index, name='index'),
    path('buying', views.buying, name='buying')

]