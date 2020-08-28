from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class doctor_profile(models.Model):
    name=models.CharField(max_length=50)
    location=models.CharField(max_length=20)
    fee=models.IntegerField()
    identification_image=models.ImageField()
    desc=models.CharField(max_length=100)
    nmc_num = models.CharField(max_length=50,default=' ')
    phone = models.CharField(max_length=50,default=' ')
    qualification = models.CharField(max_length=50,default=' ')
    speciality = models.CharField(max_length=50,default=' ')
    cat=models.ForeignKey(Category,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Symptoms(models.Model):
    sym_name=models.CharField(max_length=30)

    def __str__(self):
        return self.sym_name