from django.contrib import admin
from django.urls import path, include
from .views import feedback
from .views import ContactView

urlpatterns = [

    path('',ContactView.as_view(), name='contact'),
    path('feedback/',feedback,name='feedback')

]