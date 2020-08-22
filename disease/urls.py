from django.urls import path
from .views import SearchDisease
urlpatterns=[
    path('disease/',SearchDisease,name='disease')
]