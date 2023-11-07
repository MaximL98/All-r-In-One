from django.shortcuts import render, HttpResponse
from redditAPI import getData
# Create your views here.

def home(request):
    DF = getData()
    return render(request, "home.html", {'data': DF})

def about(request):
    return render(request, "about.html")