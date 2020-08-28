from django.shortcuts import render
from django.http import HttpResponse
from . models import doctor_profile
from . models import Symptoms
from django.contrib import messages
from math import ceil
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery
from . import views
from django.views.generic import TemplateView
from django.views.generic import DetailView
# Create your views here.
def doc(request):
    doctors = doctor_profile.objects.all()
    print(doctors)
    n=len(doctors)
    nSlides=n//4+ceil((n/4)-(n//4))
    params = {'no_of_slides':nSlides,'range':range(1,nSlides),'speciality':doctors}

    return render(request,'doctor.html', params)

def search(request):
    # query=request.GET['query']
    # speciality=doctor_profile.objects.filter(desc__icontains=query)
    # params={'speciality':speciality}
    # return render(request,'search.html',params)
    query = request.GET['query']
    if len(query) > 85:
        speciality = []
    else:
        Sname = doctor_profile.objects.filter(name__icontains=query)
        Sdesc = doctor_profile.objects.filter(desc__icontains=query)
        speciality = Sname.union(Sdesc)
    if speciality.count() == 0:
        messages.error(request, 'No Search result found. Please refine your query')

    params = {'speciality': speciality, 'query': query}
    return render(request, 'search.html', params)


def select(request):
    query=request.GET['q']
    print(query)
    disease=Symptoms.objects.filter(sym_name__icontains = query)
    para={'disease':disease, 'query': query}
    return render(request,'select.html', para)

class DoctorDetailView(DetailView):
    model = doctor_profile
    template_name='specialist/doctor_profile_detail.html'

# def category(request):
#     allProds = []
#     catprods = doctor_profile.objects.all()
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         prod = doctor_profile.objects.filter(category=cat)
#         n = len(prod)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         allProds.append([prod, range(1, nSlides), nSlides])
#
#     # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
#     # allProds = [[products, range(1, nSlides), nSlides],
#     #             [products, range(1, nSlides), nSlides]]
#     params = {'allProds': allProds}
#     return render(request, 'specialist/category.html', params)

def cat(request):
    doctors = doctor_profile.objects.all()
    print(doctors)
    # n=len(doctors)
    # nSlides=n//4+ceil((n/4)-(n//4))
    # params = {'no_of_slides':nSlides,'range':range(1,nSlides),'speciality':doctors}

    return render(request,'specialist/category.html', {'doctors':doctors})



