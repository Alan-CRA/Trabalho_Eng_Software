from django.shortcuts import render
# Create your views here.
from filmes.service import TmdbApiService
from filmes.models import Genero

def home(request):
    # api=TmdbApiService()
    # categorias=api.get_genres()
    # lista = categorias["genres"]
    # for i in lista:
    #     if not Genero.objects.filter(id=i["id"]).exists():  
    #         genero_obj, criado = Genero.objects.update_or_create(
    #                     id  =i["id"],
    #                     nome = i["name"],
    #                 )
    return render(request,'pages/home.html')

def about(request):
    return render(request,'pages/about.html')

