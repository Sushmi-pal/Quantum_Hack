from django.db import models

# Create your models here.
class Contact(models.Model):
    sn=models.AutoField(primary_key=True)
    name=models.CharField(max_length=128)
    email=models.CharField(max_length=128)
    message=models.TextField()


    def __str__(self):
        return self.name