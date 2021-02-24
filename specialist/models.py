from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()
class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class doctor_profile(models.Model):
    user=models.OneToOneField(User,unique=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    location=models.CharField(max_length=20)
    fee=models.IntegerField()
    identification_image=models.ImageField()
    desc=models.CharField(max_length=100)
    nmc_num = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class Symptoms(models.Model):
    sym_name=models.CharField(max_length=30)

    def __str__(self):
        return self.sym_name

class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    num=models.CharField(max_length=100)
    date=models.DateTimeField()
    queries=models.CharField(max_length=200,null=True)
    service=models.CharField(max_length=100)
