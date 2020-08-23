from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from .models import Contact
# Create your views here.
class ContactView(TemplateView):
    template_name = 'contact.html'

def feedback(request):
    if request.method=='POST':
        print(request.POST)
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        print(name,email,message)
        if len(name) < 1 or len(email) < 3 or len(message) == 0:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, message=message)
            contact.save()

    return render(request,'feedback.html')