from django.urls import path
from .views import ListaFilmes, Detalhes, avaliar_filme, excluir_avaliacao

app_name = "filmes"

urlpatterns = [
    path('', ListaFilmes.as_view(), name='lista_filmes'),
    path('detalhes', Detalhes.as_view(), name='detalhes'),
    path('avaliar/<int:filme_id>/', avaliar_filme, name='avaliar'),
    path('avaliar/<int:filme_id>/excluir/', excluir_avaliacao, name='excluir_avaliacao'),
]

