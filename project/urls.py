"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from htmlcss import views
from users import views as users_views
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import  login,



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls')),
    path('',views.home),
    path('index/', views.home, name='home'),
    path('specialist/',include('specialist.urls')),
    path('index/specialist/',include('specialist.urls')),
    path('testimonials/',include('testimonials.urls')),
    path('about_us/',include('about_us.urls')),
    path('contact/',include('contact.urls')),
    path('services/',include('services.urls')),
    path('register/',users_views.register ,name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('new/', views.new, name='new'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/profile/', users_views.profile, name='profile'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='registration/password_reset_done.html'),
                       name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='registration/password_reset_complete.html'),
                       name='password_reset_complete'),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
