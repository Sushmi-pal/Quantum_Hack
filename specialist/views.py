from django.shortcuts import render
from . models import doctor_profile
from math import ceil
# Create your views here.
def doc(request):
    doctors = doctor_profile.objects.all()
    print(doctors)
    n=len(doctors)
    nSlides=n//4+ceil((n/4)-(n//4))
    params = {'no_of_slides':nSlides,'range':range(1,nSlides),'speciality':doctors}

    return render(request,'doctor.html',params)
