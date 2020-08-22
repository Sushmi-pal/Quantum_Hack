from django.shortcuts import render

# Create your views here.
def SearchDisease(request):
    return render(request,'searchdisease.html')