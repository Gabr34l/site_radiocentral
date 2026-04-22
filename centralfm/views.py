import requests
from django.shortcuts import render
from django.http import JsonResponse

from .models import Promocao, Ganhador
from .utils import get_current_and_next_program, normalize_radio_text

def home(request):
    """Página inicial: Promoções, Ganhadores e Programação."""
    promocoes = Promocao.objects.filter(ativa=True)
    ganhadores = Ganhador.objects.filter(ativo=True).select_related('promocao').order_by('-data_inicio_semana', '-criado_em')[:6]
    programa_agora, proximo_programa = get_current_and_next_program()

    return render(request, 'centralfm/home.html', {
        'promocoes': promocoes,
        'ganhadores': ganhadores,
        'programa_agora': programa_agora,
        'proximo_programa': proximo_programa,
    })

def api_musica_agora(request):
    """API de Metadados: Retorna a música/locutor atual do stream."""
    url = 'https://api.brasilstream.com.br/musica_agora/id:1185863148;'
    try:
        response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        # Tenta decodificar metadados (trata encoding duplo comum em streams)
        try:
            text = response.content.decode('utf-8')
            text = text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            text = response.text

        return JsonResponse({'musica': normalize_radio_text(text)})
        
    except Exception as e:
        return JsonResponse({'musica': 'Sintonize 101.1 FM', 'erro': str(e)})
