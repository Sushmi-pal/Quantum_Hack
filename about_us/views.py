from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class InfoView(TemplateView):
    template_name = 'about_us.html'