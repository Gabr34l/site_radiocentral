"""
setup/urls.py — Roteador principal (raiz) do projeto Django.

Este arquivo é o ponto de entrada de todas as URLs do site.
Ele delega as rotas para os módulos corretos:

  /admin/   → Painel administrativo do Django (Jazzmin)
  /         → Todas as outras rotas são passadas para centralfm.urls

Em modo DEBUG (desenvolvimento local), também serve os arquivos
de mídia (fotos de locutores, ganhadores, etc.).
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Painel administrativo: acessível em /admin/ — protegido por login
    path('admin/', admin.site.urls),

    # Inclui todas as rotas do app centralfm (home, api, etc.)
    path('', include('centralfm.urls')),
]

# Em desenvolvimento, o próprio Django serve os arquivos de mídia e estáticos.
# Em produção (PythonAnywhere), o servidor web cuida disso diretamente.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
