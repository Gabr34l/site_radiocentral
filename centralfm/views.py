"""
views.py — Views (controladores) da aplicação Central FM.

Aqui ficam as funções que recebem as requisições HTTP do navegador
e decidem o que retornar: uma página HTML renderizada ou dados em JSON.

Rotas definidas neste arquivo:
  - /              → Página inicial com player, promoções e ganhadores
  - /api/musica/   → API interna que busca metadados da rádio em tempo real
"""
import requests
from django.shortcuts import render
from django.http import JsonResponse

from .models import Promocao, Ganhador
from .utils import get_current_and_next_program, normalize_radio_text


def home(request):
    """
    View da página inicial.

    Busca no banco de dados:
    - Promoções ativas para exibir no carrossel
    - Até 6 ganhadores mais recentes para a seção de destaque
    - Programa atual e o próximo da grade de programação
    """
    promocoes = Promocao.objects.filter(ativa=True)

    # Limita a 6 ganhadores, ordenados do mais recente para o mais antigo
    ganhadores = Ganhador.objects.filter(ativo=True).select_related('promocao').order_by('-data_inicio_semana', '-criado_em')[:6]

    # Calcula automaticamente qual programa está no ar agora e o próximo
    programa_agora, proximo_programa = get_current_and_next_program()

    return render(request, 'centralfm/home.html', {
        'promocoes': promocoes,
        'ganhadores': ganhadores,
        'programa_agora': programa_agora,
        'proximo_programa': proximo_programa,
    })


def api_musica_agora(request):
    """
    Endpoint JSON: /api/musica/

    Busca o nome da música/programa que está tocando agora no stream
    da BrasilStream e retorna como JSON para o player do site.

    Retorna: {"musica": "Nome da Música - Artista"}
    Em caso de erro: {"musica": "Sintonize 101.1 FM", "erro": "..."}

    Nota: O stream pode enviar texto com encoding incorreto (latin-1 tratado
    como utf-8), por isso há uma tentativa de correção automática.
    """
    url = 'https://api.brasilstream.com.br/musica_agora/id:1185863148;'
    try:
        response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        # Tenta corrigir encoding duplo (Mojibake) comum em streams de rádio
        try:
            text = response.content.decode('utf-8')
            text = text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Se a correção falhar, usa o texto original sem modificação
            text = response.text

        return JsonResponse({'musica': normalize_radio_text(text)})

    except Exception as e:
        # Fallback seguro: não quebra o site se a API da rádio estiver fora
        return JsonResponse({'musica': 'Sintonize 101.1 FM', 'erro': str(e)})
