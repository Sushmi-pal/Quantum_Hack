from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from .models import UserReview
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .models import Profile
def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'YOUR ACCOUNT HAS BEEN CREATED!YOU ARE ABLE TO LOGIN NOW')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# def reset(request):
#     return render(request,'password_reset_form.html')

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                print('user', user)
                login(request, user)
                return redirect('/profile/')
            else:
                print('Not authenticated')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/profile/')
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return redirect('/login/')


@login_required
@transaction.atomic
def ProfileView(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request,
                f'Your profile has been updated successfully'
            )
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


"""
class  receive:
    if request.method == 'POST':
        #form or something to direct the flow
        if form.is_valid():
            save_it= form.save()
            save_it.save()
            messages.success(request, f'confirmation of reservation sent to your email')
            return redirect('Here we need direct somewhere after successfull reservation')
    else:
         #form or something to direct the flow

    return render(request,'')
    """
"""
class  receive:
    if request.method == 'POST':
        #form or something to direct the flow
        if form.is_valid():
            save_it= form.save()
            save_it.save()
            messages.success(request, f'confirmation of reservation sent to your email')
            return redirect('Here we need direct somewhere after successfull reservation')
    else:
         #form or something to direct the flow

    return render(request,'')
    """


def review(request):
    con = UserReview.objects.all()
    sub = Profile.objects.all()
    sus = request.POST['query']
    models.UserReview.objects.create(review=sus)
    param = {'sus': sus, 'con': con}
    return render(request, 'review.html', param)