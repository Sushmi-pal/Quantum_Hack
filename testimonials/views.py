from django.shortcuts import render

# Create your views here.
def testimonial(request):
    return render(request,'testimonials.html')
