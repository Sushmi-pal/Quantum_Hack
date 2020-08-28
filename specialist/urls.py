from django.contrib import admin
from django.urls import path, include
from .views import doc, search, select, DoctorDetailView,cat


urlpatterns = [

    path('',doc,name='doctors'),
    path('search',search,name='search'),
    path('select',select,name='select'),
    path('detail/<int:pk>/',DoctorDetailView.as_view(),name='detail'),
    path('category/',cat)





]