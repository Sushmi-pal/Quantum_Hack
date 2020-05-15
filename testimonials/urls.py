from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.testimonial, name='testimonials'),
    path('add/',views.add,name='add'),

]