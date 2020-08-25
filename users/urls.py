from django.urls import path
from .views import review,ProfileView,LoginView,LogoutView,register


urlpatterns = [
    path('review', review, name='review'),
    path('profile/', ProfileView, name='profile'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', register, name='register')

]