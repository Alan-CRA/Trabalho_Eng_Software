from django.shortcuts import render
# Create your views here.
from filmes.service import TmdbApiService
from filmes.models import Genero

def home(request):
    return render(request,'pages/home.html')

def about(request):
    return render(request,'pages/about.html')

