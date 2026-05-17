import os
from datetime import datetime
from zoneinfo import ZoneInfo
from .models import Programa

def get_current_and_next_program():
    tz = ZoneInfo('America/Sao_Paulo')
    agora = datetime.now(tz)
    horario_atual = agora.time()
    
    dias_map = {
        0: 'segunda', 1: 'terca', 2: 'quarta', 3: 'quinta', 4: 'sexta', 5: 'sabado', 6: 'domingo'
    }
    dia_atual = dias_map[agora.weekday()]

    programa_agora = Programa.objects.filter(
        dia_semana=dia_atual,
        horario_inicio__lte=horario_atual,
        horario_fim__gte=horario_atual
    ).first()

    proximo = None
    if not programa_agora:
        proximo = Programa.objects.filter(
            dia_semana=dia_atual,
            horario_inicio__gt=horario_atual
        ).order_by('horario_inicio').first()
    else:
        proximo = Programa.objects.filter(
            dia_semana=dia_atual,
            horario_inicio__gte=programa_agora.horario_fim
        ).order_by('horario_inicio').first()

    if not proximo:
        dia_seguinte_idx = (agora.weekday() + 1) % 7
        dia_seguinte = dias_map[dia_seguinte_idx]
        proximo = Programa.objects.filter(dia_semana=dia_seguinte).order_by('horario_inicio').first()

    return programa_agora, proximo

def normalize_radio_text(text):
    if not text:
        return ""

    mapa_acentos = {
        '~a': 'ã', '~o': 'õ', '~e': 'ê', '~c': 'ç', '~n': 'ñ', 
        '~A': 'Ã', '~O': 'Õ', '~E': 'Ê', '~C': 'Ç', '~N': 'Ñ',
        '~ ': ' ',
        
        '´a': 'á', '´e': 'é', '´i': 'í', '´o': 'ó', '´u': 'ú',
        '´A': 'Á', '´E': 'É', '´I': 'Í', '´O': 'Ó', '´U': 'Ú',
        '\'a': 'á', '\'e': 'é', '\'i': 'í', '\'o': 'ó', '\'u': 'ú',
        '\'A': 'Á', '\'E': 'É', '\'I': 'Í', '\'O': 'Ó', '\'U': 'Ú',
        
        '^a': 'â', '^e': 'ê', '^i': 'î', '^o': 'ô', '^u': 'û',
        '^A': 'Â', '^E': 'Ê', '^I': 'Î', '^O': 'Ô', '^U': 'Û',
        
        '`a': 'à', '`e': 'è', '`i': 'ì', '`o': 'ò', '`u': 'ù',
        '`A': 'À', '`E': 'È', '`I': 'Ì', '`O': 'Ò', '`U': 'Ù',
        
        '&amp;': '&', '&#039;': "'", '&quot;': '"', '&lt;': '<', '&gt;': '>',
    }

    text = text.strip()
    for erro, acerto in mapa_acentos.items():
        text = text.replace(erro, acerto)
        
    if text.isupper():
        text = text.title()
        
    return text.strip()
