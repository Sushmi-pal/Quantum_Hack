from django.shortcuts import render,redirect
from .models import entry
from .forms import entryForm
# Create your views here.
def testimonial(request):
    ent = entry.objects.order_by('-date_posted')
    return render(request,'testimonials.html',{'ent':ent})
def add(request):
    if request.method=='POST':
        form = entryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('testimonials')
    else:
        form = entryForm()

        return render(request,'add.html',{'form':form})