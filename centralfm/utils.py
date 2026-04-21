import os
from datetime import datetime
from zoneinfo import ZoneInfo
from .models import Programa

def get_current_and_next_program():
    """
    Identifica qual programa está no ar e qual será a próxima atração
    com base no fuso horário de Brasília (São Paulo).
    """
    # Define o fuso horário oficial da rádio
    tz = ZoneInfo('America/Sao_Paulo')
    agora = datetime.now(tz)
    horario_atual = agora.time()
    
    # Converte o dia da semana do Python (0=segunda) para o padrão do nosso modelo
    dias_map = {
        0: 'segunda', 1: 'terca', 2: 'quarta', 3: 'quinta', 4: 'sexta', 5: 'sabado', 6: 'domingo'
    }
    dia_atual = dias_map[agora.weekday()]

    # Localiza o programa que abrange o horário atual no dia correto
    programa_agora = Programa.objects.filter(
        dia_semana=dia_atual,
        horario_inicio__lte=horario_atual,
        horario_fim__gte=horario_atual
    ).first()

    # Identifica a próxima atração
    proximo = None
    if not programa_agora:
        # Se não há programa agora, busca o primeiro que começa depois do horário atual
        proximo = Programa.objects.filter(
            dia_semana=dia_atual,
            horario_inicio__gt=horario_atual
        ).order_by('horario_inicio').first()
    else:
        # Se há programa agora, busca o próximo do mesmo dia
        proximo = Programa.objects.filter(
            dia_semana=dia_atual,
            horario_inicio__gte=programa_agora.horario_fim
        ).order_by('horario_inicio').first()

    # Caso não haja mais nada no dia atual, busca o primeiro do dia seguinte
    if not proximo:
        dia_seguinte_idx = (agora.weekday() + 1) % 7
        dia_seguinte = dias_map[dia_seguinte_idx]
        proximo = Programa.objects.filter(dia_semana=dia_seguinte).order_by('horario_inicio').first()

    return programa_agora, proximo

def normalize_radio_text(text):
    """
    Remove artefatos de codificação comuns em metadados de rádio
    e normaliza acentos e caracteres especiais do alfabeto.
    """
    if not text:
        return ""

    mapa_acentos = {
        # Til (~)
        '~a': 'ã', '~o': 'õ', '~e': 'ê', '~c': 'ç', '~n': 'ñ', 
        '~A': 'Ã', '~O': 'Õ', '~E': 'Ê', '~C': 'Ç', '~N': 'Ñ',
        '~ ': ' ',
        
        # Agudo (´ e ')
        '´a': 'á', '´e': 'é', '´i': 'í', '´o': 'ó', '´u': 'ú',
        '´A': 'Á', '´E': 'É', '´I': 'Í', '´O': 'Ó', '´U': 'Ú',
        '\'a': 'á', '\'e': 'é', '\'i': 'í', '\'o': 'ó', '\'u': 'ú',
        '\'A': 'Á', '\'E': 'É', '\'I': 'Í', '\'O': 'Ó', '\'U': 'Ú',
        
        # Circunflexo (^)
        '^a': 'â', '^e': 'ê', '^i': 'î', '^o': 'ô', '^u': 'û',
        '^A': 'Â', '^E': 'Ê', '^I': 'Î', '^O': 'Ô', '^U': 'Û',
        
        # Grave (`)
        '`a': 'à', '`e': 'è', '`i': 'ì', '`o': 'ò', '`u': 'ù',
        '`A': 'À', '`E': 'È', '`I': 'Ì', '`O': 'Ò', '`U': 'Ù',
        
        # Entidades HTML e outros
        '&amp;': '&', '&#039;': "'", '&quot;': '"', '&lt;': '<', '&gt;': '>',
    }

    text = text.strip()
    for erro, acerto in mapa_acentos.items():
        text = text.replace(erro, acerto)
        
    # Estética: Se vier tudo em MAIÚSCULAS, converte para Capitalizado
    if text.isupper():
        text = text.title()
        
    return text.strip()
