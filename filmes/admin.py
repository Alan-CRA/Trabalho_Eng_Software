from django.contrib import admin
from django.conf import settings
# Register your models here.
from .models import Filme,Genero,Avaliacao,Ator,Streaming

admin.site.register(Filme)
admin.site.register(Genero)
admin.site.register(Avaliacao)
admin.site.register(Ator)
admin.site.register(Streaming)

