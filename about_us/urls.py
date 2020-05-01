from django.contrib import admin
from django.urls import path, include
from . import views
from .views import InfoView

urlpatterns = [
    path('', InfoView.as_view(), name='about_us'),
]