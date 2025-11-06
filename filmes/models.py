from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Genero(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.nome

class Ator(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    def __str__(self): return self.nome

class Streaming(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    def __str__(self): return self.nome

class Filme(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    nome = models.CharField(max_length=255)
    lancamento = models.CharField(max_length=20, blank=True, null=True)
    tempo = models.PositiveIntegerField(blank=True, null=True)  # minutos
    sinopse = models.TextField(blank=True, null=True)
    nota_media = models.FloatField(blank=True, null=True)
    poster_path = models.CharField(max_length=300, blank=True, null=True)
    backdrop_path = models.CharField(max_length=300, blank=True, null=True)

    genero = models.ManyToManyField(Genero, blank=True)
    atores = models.ManyToManyField(Ator, blank=True)
    streaming = models.ManyToManyField(Streaming, blank=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.tmdb_id})"

    def poster_url(self, size='w342', base=None):
        base = base or "https://image.tmdb.org/t/p/"
        return f"{base}{size}{self.poster_path}" if self.poster_path else ""

    def backdrop_url(self, size='w780', base=None):
        base = base or "https://image.tmdb.org/t/p/"
        return f"{base}{size}{self.backdrop_path}" if self.backdrop_path else ""

class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField()  # 1..10
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'filme')

    def __str__(self):
        return f"{self.user} - {self.filme} ({self.nota})"
