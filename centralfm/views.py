import urllib.request
from django.shortcuts import render
from django.http import JsonResponse

from .models import Promocao, Ganhador
from .utils import get_current_and_next_program, normalize_radio_text

def home(request):
    """
    Página inicial do site.
    Carrega as promoções ativas, os ganhadores da semana e define qual programa está no ar agora.
    """
    promocoes = Promocao.objects.filter(ativa=True)
    
    # Busca os 6 ganhadores mais recentes ativos
    ganhadores = Ganhador.objects.filter(ativo=True).select_related('promocao').order_by('-data_inicio_semana', '-criado_em')[:6]
    
    programa_agora, proximo_programa = get_current_and_next_program()

    context = {
        'promocoes': promocoes,
        'ganhadores': ganhadores,
        'programa_agora': programa_agora,
        'proximo_programa': proximo_programa,
    }
    return render(request, 'centralfm/home.html', context)

def api_musica_agora(request):
    """
    API que retorna o nome da música que está tocando no rádio em tempo real.
    A API consome o metadado do stream através do BrasilStream.
    """
    try:
        url = 'https://api.brasilstream.com.br/musica_agora/id:1185863148;'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=5) as resp:
            raw_data = resp.read()
            # Tenta UTF-8 primeiro, depois Latin-1 como fallback
            try:
                text = raw_data.decode('utf-8')
                try:
                    text = text.encode('latin-1').decode('utf-8') # Resolve "Double-Encoding"
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass
            except UnicodeDecodeError:
                text = raw_data.decode('latin-1')
        
        # Limpa e normaliza os acentos de todo o alfabeto usando a lógica do utils.py
        text_clean = normalize_radio_text(text)
            
        return JsonResponse({'musica': text_clean})
        
    except Exception as e:
        # Se houver erro, retorna um fallback genérico
        return JsonResponse({'musica': 'Sintonize 101.1 FM', 'erro': str(e)})
