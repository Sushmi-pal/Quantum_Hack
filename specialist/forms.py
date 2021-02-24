from django import forms
from django.forms import ModelForm
from .models import Appointment
# class DoctorRegisterForm(forms.ModelForm):
#     username=models.CharField(max_length=100)
#     password1=models
#     class Meta:
#         model=doctor_profile
#         fields=['username','password1','password2','name','location','fee','identification_image','desc','nmc_num','phone','qualification','speciality']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['full_name', 'num', 'date', 'queries', 'service']