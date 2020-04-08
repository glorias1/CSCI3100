from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, 'webpage/home.html')