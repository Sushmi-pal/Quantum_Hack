from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from . models import doctor_profile
from . models import Symptoms, Appointment
from django.contrib import messages
from math import ceil
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery
from . import views
from django.views.generic import TemplateView
from django.views.generic import DetailView
from users.models import Doctor
from .forms import AppointmentForm
from django.template.loader import get_template
from django.core.mail import send_mail,EmailMultiAlternatives

# from .forms import DoctorRegisterForm
# Create your views here.
def doc(request):
    doctors = Doctor.objects.all()
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
        Sname = Doctor.objects.filter(name__icontains=query)
        Sdesc = Doctor.objects.filter(desc__icontains=query)
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
    model = Doctor
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


# def docregister(request):
#     if request.method == 'POST':
#         form = DoctorRegisterForm(request.POST,request.FILES)
#         print(request.POST)
#         print(type(request.POST))
#         print(form.errors)
#         if form.is_valid():
#             print('valid')
#             form.save()
#             return redirect('login')
#         else:
#             print(form.errors)
#             print('Not valid')
#     else:
#         form = DoctorRegisterForm()
#     return render(request, 'specialist/doctor_register.html', {'form': form})

def appointment(request):
    name = request.session.get('name')
    phoneno = request.session.get('phoneno')
    service = request.session.get('service')
    date = request.session.get('date')
    message = request.session.get('message')
    print(name)
    return render (request,'specialist/appointment.html',{'name':name,'phoneno':phoneno,'service':service,'date':date,'message':message})

def bookappointment(request):
    html_file = get_template('specialist/n.html')
    html_content = html_file.render()
    sub = 'Appointment'
    from_email = 'sushpalikhe85@gmail.com'
    to = ['sushmipalikhe97@gmail.com', ]
    msg = EmailMultiAlternatives(subject=sub, from_email=from_email, to=to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    if request.method == 'POST':
        name = request.POST['name']
        phoneno = request.POST['phoneno']
        service = request.POST['service']
        date = request.POST['date']
        message = request.POST['message']
        request.session['name'] = name
        request.session['phoneno'] = phoneno
        request.session['service'] = service
        request.session['date'] = date
        request.session['message'] = message
        ap=Appointment(full_name=name,num=phoneno,date=date,queries=message, service=service)
        ap.save()
        global val
        def val():
            # context={'name':name,'phoneno':phoneno,'service':service,'date':date,'message':message}
            return name
        # form = AppointmentForm(request.POST)
        # print(form)
        # if form.is_valid():
        #     form.save()
        messages.success(request, f'YOUR APPOINTMENT HAS BEEN MADE')
        return redirect ('bookappointment')

    else:
        form = AppointmentForm()
    return render(request, 'specialist/book.html', {'form': form})
