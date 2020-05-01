from django.db import models

# Create your models here.
class doctor_profile(models.Model):
    name=models.CharField(max_length=20)
    location=models.CharField(max_length=20)
    fee=models.IntegerField()
    identification_image=models.ImageField()
    desc=models.CharField(max_length=100)

    def __str__(self):
        return self.name