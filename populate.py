"""
populate.py — Script de população inicial do banco de dados.

Este script cria automaticamente todos os Locutores e Programas
da grade de programação da Rádio Central FM 101.1 no banco de dados.

USO:
    python populate.py

ATENÇÃO:
    O script APAGA todos os Programas existentes antes de recriar (linha 65).
    Rode apenas quando quiser resetar a grade de programação do zero.
    Os Locutores são criados com get_or_create (não duplica se já existirem).

Dias cobertos: Segunda a Sexta (grade padrão), Sábado e Domingo.
"""
import os
import django
from datetime import time

# Configura o Django antes de importar qualquer model
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from centralfm.models import Locutor, Programa

# Locutores
loc_nomes = [
    "Danilo Vilela", "Chicão", "Alex Silva", "Renata Lima", 
    "Cairo Santos", "Igreja Evangélica", "Padre Aldemir - Igreja Católica",
    "Centro Espírita", "Igreja Evangélica (Jovens)", "Canal Gov"
]

locutores = {}
for nome in loc_nomes:
    obj, _ = Locutor.objects.get_or_create(nome=nome)
    locutores[nome] = obj

# Grade de Segunda a Sexta
dias_uteis = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']

Grade = []

for dia in dias_uteis:
    Grade.extend([
        {"nome": "Madrugada 101", "locutor": None, "dia": dia, "inicio": time(0,0), "fim": time(5,0)},
        {"nome": "Show da Manhã", "locutor": locutores["Danilo Vilela"], "dia": dia, "inicio": time(5,0), "fim": time(8,0)},
        {"nome": "Top Central", "locutor": locutores["Chicão"], "dia": dia, "inicio": time(8,0), "fim": time(11,0)},
        {"nome": "A Voz das Assembleias", "locutor": locutores["Igreja Evangélica"], "dia": dia, "inicio": time(11,0), "fim": time(11,30)},
        {"nome": "Jornal da Central", "locutor": locutores["Alex Silva"], "dia": dia, "inicio": time(11,30), "fim": time(13,0)},
        {"nome": "Central Alegre", "locutor": locutores["Alex Silva"], "dia": dia, "inicio": time(13,0), "fim": time(16,0)},
        {"nome": "Alô Central", "locutor": locutores["Cairo Santos"], "dia": dia, "inicio": time(16,0), "fim": time(18,0)},
        {"nome": "Noite 101", "locutor": locutores["Renata Lima"], "dia": dia, "inicio": time(18,0), "fim": time(21,0)},
        {"nome": "A Voz do Brasil", "locutor": locutores["Canal Gov"], "dia": dia, "inicio": time(21,0), "fim": time(22,0)},
        {"nome": "Madrugada 101", "locutor": None, "dia": dia, "inicio": time(22,0), "fim": time(23,59,59)},
    ])

# Sábado
Grade.extend([
    {"nome": "101 Mais Tocadas", "locutor": None, "dia": 'sabado', "inicio": time(0,0), "fim": time(6,0)},
    {"nome": "Show da Manhã", "locutor": locutores["Danilo Vilela"], "dia": 'sabado', "inicio": time(6,0), "fim": time(8,0)},
    {"nome": "Top Central", "locutor": locutores["Chicão"], "dia": 'sabado', "inicio": time(8,0), "fim": time(11,0)},
    {"nome": "Criança Feliz", "locutor": locutores["Igreja Evangélica"], "dia": 'sabado', "inicio": time(11,0), "fim": time(11,30)},
    {"nome": "Meia Hora de Sucesso", "locutor": None, "dia": 'sabado', "inicio": time(11,30), "fim": time(12,0)},
    {"nome": "Central Alegre", "locutor": locutores["Alex Silva"], "dia": 'sabado', "inicio": time(12,0), "fim": time(15,0)},
    {"nome": "Alto Astral", "locutor": locutores["Renata Lima"], "dia": 'sabado', "inicio": time(15,0), "fim": time(18,0)},
    {"nome": "101 Mais Tocadas", "locutor": None, "dia": 'sabado', "inicio": time(18,0), "fim": time(23,59,59)}, 
])

# Domingo
Grade.extend([
    {"nome": "101 Mais Tocadas", "locutor": None, "dia": 'domingo', "inicio": time(0,0), "fim": time(6,0)},
    {"nome": "Domingo Show", "locutor": locutores["Cairo Santos"], "dia": 'domingo', "inicio": time(6,0), "fim": time(9,0)},
    {"nome": "Santa Missa", "locutor": locutores["Padre Aldemir - Igreja Católica"], "dia": 'domingo', "inicio": time(9,0), "fim": time(10,0)},
    {"nome": "Domingo Show", "locutor": locutores["Cairo Santos"], "dia": 'domingo', "inicio": time(10,0), "fim": time(12,0)},
    {"nome": "Ondas de Luz", "locutor": locutores["Centro Espírita"], "dia": 'domingo', "inicio": time(12,0), "fim": time(12,30)},
    {"nome": "Jovens Vencedores", "locutor": locutores["Igreja Evangélica (Jovens)"], "dia": 'domingo', "inicio": time(12,30), "fim": time(13,0)},
    {"nome": "Domingão Central", "locutor": None, "dia": 'domingo', "inicio": time(13,0), "fim": time(18,0)},
    {"nome": "101 Mais Tocadas", "locutor": None, "dia": 'domingo', "inicio": time(18,0), "fim": time(23,59,59)},
])

Programa.objects.all().delete() # Limpa tudo primeiro

for p in Grade:
    Programa.objects.create(
        nome=p['nome'],
        locutor=p['locutor'],
        dia_semana=p['dia'],
        horario_inicio=p['inicio'],
        horario_fim=p['fim']
    )

print("Dados populados com sucesso!")
