from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('filmes/', include('filmes.urls')),
    path('contas/', include('contas.urls')),
]
