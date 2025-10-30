from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    senhaHash = models.CharField(max_length=255)

    def avaliar(self, filme, nota, comentario):
        from filmes.models import Avaliacao
        return Avaliacao.objects.create(usuario=self, filme=filme, nota=nota, comentario=comentario)
