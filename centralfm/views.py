import requests
from django.shortcuts import render
from django.http import JsonResponse

from .models import Promocao, Ganhador, Programa, Locutor
from .utils import get_current_and_next_program, normalize_radio_text


def home(request):
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
    url = 'https://api.brasilstream.com.br/musica_agora/id:1185863148;'
    try:
        response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        try:
            text = response.content.decode('utf-8')
            text = text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            text = response.text

        return JsonResponse({'musica': normalize_radio_text(text)})

    except Exception as e:
        return JsonResponse({'musica': 'Sintonize 101.1 FM', 'erro': str(e)})


def api_programacao(request):
    programa_agora, proximo_programa = get_current_and_next_program()
    
    agora_data = {
        'nome': programa_agora.nome if programa_agora else '101 Mais Tocadas',
        'locutor_nome': programa_agora.apresentador_atual.nome if programa_agora and programa_agora.apresentador_atual else 'Equipe Central',
        'locutor_foto': programa_agora.apresentador_atual.media_url if programa_agora and programa_agora.apresentador_atual and programa_agora.apresentador_atual.media_url else '',
    }
    
    proximo_data = {
        'nome': proximo_programa.nome if proximo_programa else 'Programação Especial',
        'locutor_nome': proximo_programa.apresentador_atual.nome if proximo_programa and proximo_programa.apresentador_atual else 'Equipe Central',
        'locutor_foto': proximo_programa.apresentador_atual.media_url if proximo_programa and proximo_programa.apresentador_atual and proximo_programa.apresentador_atual.media_url else '',
        'horario': f"{proximo_programa.horario_inicio.hour}h" if proximo_programa and proximo_programa.horario_inicio else '',
    }
    
    return JsonResponse({'agora': agora_data, 'proximo': proximo_data})
