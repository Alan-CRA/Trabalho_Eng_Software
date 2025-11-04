from django.urls import path
from .views import ListaFilmes, Detalhes

app_name = "filmes"

urlpatterns = [
    path('', ListaFilmes.as_view(), name='lista_filmes'),
    path('detalhes', Detalhes.as_view(), name='detalhes'),
]
