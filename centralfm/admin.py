from django.contrib import admin
from .models import Locutor, Promocao, Programa, Ganhador

# ADMIN: Locutores
@admin.register(Locutor)
class LocutorAdmin(admin.ModelAdmin):
    """
    Interface para gerenciar os locutores da rádio.
    Permite busca por nome e exibe a foto, se houver.
    """
    list_display = ('nome', 'tem_foto')
    search_fields = ('nome',)

    def tem_foto(self, obj):
        return bool(obj.foto)
    tem_foto.boolean = True
    tem_foto.short_description = 'Possui Foto?'

# ADMIN: Promoções
@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    """
    Gerencia as miniaturas e banners que aparecem no carrossel de promoções.
    """
    list_display = ('titulo', 'ativa', 'criada_em')
    list_editable = ('ativa',)

    list_filter = ('ativa',)
    search_fields = ('titulo',)

# ADMIN: Ganhadores da Semana
@admin.register(Ganhador)
class GanhadorAdmin(admin.ModelAdmin):
    """
    Interface para cadastro dos ganhadores das promoções.
    """
    list_display = ('nome', 'promocao', 'data_inicio_semana', 'data_fim_semana', 'ativo')
    list_editable = ('ativo',)
    list_filter = ('promocao', 'ativo', 'data_inicio_semana')
    search_fields = ('nome',)
    
    fieldsets = (
        ('DADOS DO GANHADOR', {
            'fields': ('nome', 'foto')
        }),
        ('PROMOÇÃO E PERÍODO', {
            'fields': ('promocao', 'data_inicio_semana', 'data_fim_semana')
        }),

        ('VISIBILIDADE', {
            'fields': ('ativo',)
        }),
    )

# ADMIN: Grade de Programas

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    """
    Gerencia a grade de horários da rádio.
    Facilita a visualização do dia da semana e horários de cada atração.
    """
    list_display = ('nome', 'dia_semana', 'horario_inicio', 'horario_fim', 'locutor')
    list_filter = ('dia_semana', 'locutor')
    search_fields = ('nome',)
    ordering = ('dia_semana', 'horario_inicio')
