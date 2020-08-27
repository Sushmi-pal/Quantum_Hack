from django.urls import path
from .views import SearchDisease,checkdisease
urlpatterns=[
    path('disease/',SearchDisease,name='disease'),
    path('checkdisease/',checkdisease,name='checkdisease')
]