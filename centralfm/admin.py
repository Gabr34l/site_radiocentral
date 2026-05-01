"""
admin.py — Configuração do painel administrativo do Django.

Este arquivo registra os models no Django Admin e personaliza
a forma como cada um é exibido, filtrado e editado pelos administradores
do site da Rádio Central FM 101.1.
"""
from django.contrib import admin
from .models import Locutor, Promocao, Programa, Ganhador

# ─── LOCUTOR ────────────────────────────────────────────────────────────────
# Exibe os locutores cadastrados com um indicador visual (✓/✗) de foto.
@admin.register(Locutor)
class LocutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tem_foto', 'tem_gif_animado')
    search_fields = ('nome',)

    fieldsets = (
        ('DADOS DO LOCUTOR', {'fields': ('nome',)}),
        ('MÍDIA', {
            'fields': ('foto', 'gif_animado'),
            'description': 'O GIF animado, se preenchido, substitui a foto no site.'
        }),
    )

    def tem_foto(self, obj):
        """Retorna True/False para exibir ✓ ou ✗ na coluna 'Foto?' da listagem."""
        return bool(obj.foto)
    tem_foto.boolean = True
    tem_foto.short_description = 'Foto?'

    def tem_gif_animado(self, obj):
        """Retorna True/False para exibir ✓ ou ✗ na coluna 'GIF?' da listagem."""
        return bool(obj.gif_animado)
    tem_gif_animado.boolean = True
    tem_gif_animado.short_description = 'GIF?'

# ─── PROMOÇÃO ───────────────────────────────────────────────────────────────
# Permite ativar/desativar promoções diretamente na listagem (list_editable)
# sem precisar abrir o formulário completo de edição.
@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa', 'criada_em')
    list_editable = ('ativa',)   # Edição rápida do status na listagem
    list_filter = ('ativa',)
    search_fields = ('titulo',)

# ─── GANHADOR ───────────────────────────────────────────────────────────────
# Formulário organizado em seções (fieldsets) para facilitar o cadastro
# de novos ganhadores sem confundir quem administra o painel.
@admin.register(Ganhador)
class GanhadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'promocao', 'data_inicio_semana', 'ativo')
    list_editable = ('ativo',)   # Liga/desliga a exibição no site diretamente na lista
    list_filter = ('promocao', 'ativo', 'data_inicio_semana')
    search_fields = ('nome',)

    # Divide o formulário em grupos visuais para melhor usabilidade
    fieldsets = (
        ('DADOS DO GANHADOR', {'fields': ('nome', 'foto')}),
        ('PROMOÇÃO E PERÍODO', {'fields': ('promocao', 'data_inicio_semana', 'data_fim_semana')}),
        ('VISIBILIDADE', {'fields': ('ativo',)}),
    )

# ─── PROGRAMA ───────────────────────────────────────────────────────────────
# A grade de programação. Ordenada por dia da semana e horário de início
# para facilitar a visualização da grade completa.
@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dia_semana', 'horario_inicio', 'horario_fim', 'locutor')
    list_filter = ('dia_semana', 'locutor')   # Filtros laterais para navegação rápida
    search_fields = ('nome',)
    ordering = ('dia_semana', 'horario_inicio')
