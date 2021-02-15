from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Patient,Doctor
User=get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.CharField()
    sex = forms.ChoiceField(choices=[('MALE','male'),('FEMALE','female')])

    class Meta:
        model = User
        fields = ['username','email','age','sex','password1','password2']

class UserUpdateForm(forms.ModelForm):



    class Meta:
        model = User
        fields = ['username','email']



class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['name', 'location', 'fee', 'desc', 'nmc_num', 'phone', 'qualification', 'speciality']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']



class LoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(max_length=128,widget=forms.PasswordInput())

class DoctorSignupForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    location = forms.CharField(max_length=20)
    fee = forms.IntegerField()
    identification_image = forms.ImageField()
    desc = forms.CharField(max_length=100)
    nmc_num = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)
    qualification = forms.CharField(max_length=50)
    speciality = forms.CharField(max_length=50)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user

class PatientSignUpForm(UserCreationForm):
    Choices=(
        ('M','Male'),
        ('F','Female'))
    age=forms.IntegerField()
    gender = forms.ChoiceField(choices=Choices)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user