from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Genero(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Streaming(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Ator(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Filme(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    sinopse = models.TextField()
    nota_media = models.FloatField()
    generos = models.ManyToManyField(Genero, related_name="filmes")
    atores = models.ManyToManyField(Ator, related_name="filmes")
    streaming = models.ManyToManyField(Streaming, related_name="filmes")
    lancamento = models.CharField(max_length=10)
    poster = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.nome
    
    def filtrar(self):
        pass
    def get_movies_images_M(self):
        if self.poster:
            return 'https://image.tmdb.org/t/p/w200' + self.poster
    def get_movies_images_G(self):
        if self.poster:
            return 'https://image.tmdb.org/t/p/w500' + self.poster
    

class Avaliacao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name="avaliacoes")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avaliacoes")
    nota = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.filme.nome} ({self.nota})"
