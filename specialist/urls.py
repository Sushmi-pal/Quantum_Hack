from django.contrib import admin
from django.urls import path, include
from .views import doc, search, select, DoctorDetailView,cat,appointment,bookappointment


urlpatterns = [

    path('',doc,name='doctors'),
    path('search',search,name='search'),
    path('select',select,name='select'),
    path('detail/<int:pk>/',DoctorDetailView.as_view(),name='detail'),
    path('book',bookappointment,name='bookappointment'),
    path('appointment',appointment,name='appointment'),
    path('category/',cat),
    # path('doctor_register',docregister)





]