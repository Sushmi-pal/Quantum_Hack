from django.urls import path
from .views import review,ProfileView,PatientLoginView, DoctorLoginView,LogoutView,register,docregister,patientregister,DProfileView


urlpatterns = [
    path('review', review, name='review'),
    path('profile/', ProfileView, name='profile'),
    path('patientlogin/', PatientLoginView, name='patientlogin'),
    path('doctorlogin/', DoctorLoginView, name='doctorlogin'),
    path('logout/', LogoutView, name='logout'),
    path('register/', register, name='register'),
    path('docr',docregister,name='doctorregister'),
    path('patr',patientregister,name='patientregister'),
    path('dprofile',DProfileView,name='dprofile')

]