from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, \
    PatientSignUpForm, DoctorUpdateForm
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from .models import UserReview
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, DoctorSignupForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .models import Profile, Patient, Doctor
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User=get_user_model()
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

def PatientLoginView(request):
    if request.method == 'POST' :
        print(request.user.id)
        form = LoginForm(request.POST)
        print(request.POST)
        print('password',request.POST.get('password'))

        print(form)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))

            if user:
                print('user', user)

                login(request, user)
                return redirect('/profile/')
            else:
                print('Not authenticated')

    elif request.method == 'GET':
        form = LoginForm()
    return render(request, 'users/patientlogin.html', {'form': form})


def DoctorLoginView(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        print(request.POST)
        print('password',request.POST.get('password'))

        print(form)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))

            if user:
                print('user', user)

                login(request, user)
                return redirect('/profile/')
            else:
                print('Not authenticated')

    elif request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/doctorlogin.html', {'form': form})

def LogoutView(request):
    logout(request)
    return redirect('/login/')


@login_required
@transaction.atomic
def ProfileView(request):
    if request.method == 'POST':
        print(request.user.id)
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
        'p_form': p_form,

    }
    return render(request, 'users/profile.html', context)

@login_required
@transaction.atomic
def DProfileView(request):
    # if request.method == 'POST':
    #     print(request.user)
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #     z_form = DoctorUpdateForm(request.POST, instance=request.user)
    #     if u_form.is_valid() and p_form.is_valid() and z_form.is_valid():
    #         u_form.save()
    #
    #         p_form.save()
    #         z_form.save()
    #
    #         messages.success(
    #             request,
    #             f'Your profile has been updated successfully'
    #         )
    #         return redirect('dprofile')
    #
    #
    # else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    z_form = DoctorUpdateForm(instance=request.user)
    print(u_form)
    print(p_form)
    print(z_form)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'z_form': z_form
    }
    return render(request, 'users/doctorprofile.html', context)


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

def docregister(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST,request.FILES)
        print(request.POST)
        print(request.FILES)
        username = request.POST.get('username')
        image=request.FILES.get('identification_image')
        print('image',image)
        print('username', username)
        password1 = request.POST.get('password1')
        print(password1)
        password2 = request.POST.get('password2')
        print('password1', password1)
        print('password2', password2)
        p1=make_password(password1)
        p2=make_password(password2)
        name = request.POST.get('name')
        location = request.POST.get('location')
        fee = request.POST.get('fee')
        desc = request.POST.get('desc')
        nmc_num = request.POST.get('nmc_num')
        phone = request.POST.get('phone')
        qualification = request.POST.get('qualification')
        speciality = request.POST.get('speciality')
        is_patient = False
        is_doctor = True
        u = User.objects.create(username=username, password=p1, confirm_password=p2,
                                is_patient=is_patient, is_doctor=is_doctor)


        if is_doctor:
            d = Doctor.objects.create(user=u, name=name,location=location,identification_image=image,fee=fee,
                                      desc=desc, nmc_num=nmc_num, phone=phone, qualification=qualification,speciality=speciality)
            d.save()
            return redirect('login')


        print(form.errors)
        if form.is_valid():
            print('valid')

            form.save()
            return redirect('login')
        else:
            print(form.errors)
            print('Not valid')
    else:
        form = DoctorSignupForm()
    return render(request, 'specialist/doctor_register.html', {'form': form})

def patientregister(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        print(request.POST)
        username=request.POST.get('username')
        print('username',username)
        password1=request.POST.get('password1')
        print(password1)
        password2=request.POST.get('password2')
        print('password1',password1)
        print('password2',password2)
        p1=make_password(password1)
        p2=make_password(password2)
        print(p1)
        print(p2)

        
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        is_patient=True
        is_doctor=False
        u = User.objects.create(username=username, password=p1, confirm_password=p2,is_patient=is_patient,is_doctor=is_doctor)
        print(is_doctor)
        print(is_patient)

        if is_patient:
            p=Patient.objects.create(user=u,age=age,gender=gender)
            p.save()
            return redirect('login')

        print(form.errors)
        if form.is_valid():
            print('valid')

            form.save()
            return redirect('login')
        else:
            print(form.errors)
            print('Not valid')
    else:
        form = PatientSignUpForm()
    return render(request, 'users/patientregister.html', {'form': form})
