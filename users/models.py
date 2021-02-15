
# Create your models here.
#The script is used for creating models for app.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    confirm_password = models.CharField(max_length=128, null=True)
    is_doctor=models.BooleanField(default=False)
    is_patient=models.BooleanField(default=False)

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    fee = models.IntegerField()
    identification_image = models.ImageField(upload_to='d_pics')
    desc = models.CharField(max_length=100)
    nmc_num = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user.is_doctor=True
        super(Doctor, self).save(*args, **kwargs)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.IntegerField()
    Choices=(
        ('M','Male'),
        ('F','Female'))
    gender=models.CharField(max_length=100,choices=Choices)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        unique=True,
        related_name='profile',
        on_delete=models.CASCADE
        )
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics'
        )


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)    
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserReview(models.Model):
    review=models.TextField()

    def __str__(self):
        return self.review
