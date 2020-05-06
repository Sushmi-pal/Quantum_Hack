from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.doc,name='doctors'),
    path('search',views.search,name='search'),
    path('select',views.select,name='select'),




]