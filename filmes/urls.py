from django.urls import path

from . import views

urlpatterns = [
    path('',views.lista_filmes,name="lista_filmes"),
    path('detalhe/',views.detalhes,name="detalhes")
]