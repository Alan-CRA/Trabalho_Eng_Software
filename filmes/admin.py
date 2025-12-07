from django.contrib import admin
from .models import Filme, Genero, Ator, Streaming, Avaliacao

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ("tmdb_id","nome","lancamento","nota_media","atualizado_em")
    search_fields = ("nome",)

admin.site.register(Genero)
admin.site.register(Ator)
admin.site.register(Streaming)
admin.site.register(Avaliacao)
