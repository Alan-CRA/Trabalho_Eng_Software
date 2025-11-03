from django.urls import path
from .views import Entrar, Registrar, sair, perfil

app_name = "contas"

urlpatterns = [
    path('entrar/', Entrar.as_view(), name='entrar'),
    path('registrar/', Registrar.as_view(), name='registrar'),
    path('sair/', sair, name='sair'),
    path('usuario/', perfil, name='perfil'),
]
