from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class diseaseinfo(models.Model):

    user = models.ForeignKey(User , null=True, on_delete=models.SET_NULL)

    diseasename = models.CharField(max_length = 200)
    no_of_symp = models.IntegerField()
    symptomsname = ArrayField(models.CharField(max_length=200))
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200)
