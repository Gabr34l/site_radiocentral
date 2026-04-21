from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/musica/', views.api_musica_agora, name='api_musica_agora'),
]
