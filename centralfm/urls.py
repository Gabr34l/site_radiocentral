"""
urls.py — Mapeamento de URLs da aplicação centralfm.

Define quais endereços (URLs) o Django deve reconhecer e qual
função (view) deve ser chamada para cada um.

  /              → Página inicial do site
  /api/musica/   → API interna que retorna a música atual do stream
"""
from django.urls import path
from . import views

urlpatterns = [
    # Página inicial: exibe o player, promoções, ganhadores e grade de programação
    path('', views.home, name='home'),

    # Endpoint usado pelo JavaScript do player para buscar metadados da música atual
    path('api/musica/', views.api_musica_agora, name='api_musica_agora'),
]
