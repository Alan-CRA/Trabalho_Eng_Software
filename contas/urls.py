from django.urls import path
from .views import Entrar, Registrar, sair, perfil, minhas_avaliacoes, meus_favoritos

app_name = "contas"

urlpatterns = [
    path('entrar/', Entrar.as_view(), name='entrar'),
    path('registrar/', Registrar.as_view(), name='registrar'),
    path('sair/', sair, name='sair'),
    path('usuario/', perfil, name='perfil'),
    path('usuario/avaliacoes/', minhas_avaliacoes, name='minhas_avaliacoes'),
    path('usuario/favoritos/', meus_favoritos, name='meus_favoritos'),
]

