# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import Locutor, Promocao, Programa, Ganhador

@admin.register(Locutor)
class LocutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tem_foto', 'tem_gif_animado')
    search_fields = ('nome',)

    fieldsets = (
        ('DADOS DO LOCUTOR', {'fields': ('nome', 'bio', 'instagram')}),
        ('MÍDIA', {
            'fields': ('foto', 'gif_animado'),
            'description': 'O GIF animado, se preenchido, substitui a foto no site.'
        }),
    )

    def tem_foto(self, obj):
        return bool(obj.foto)
    tem_foto.boolean = True
    tem_foto.short_description = 'Foto?'

    def tem_gif_animado(self, obj):
        return bool(obj.gif_animado)
    tem_gif_animado.boolean = True
    tem_gif_animado.short_description = 'GIF?'


@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa', 'criada_em')
    list_editable = ('ativa',)
    list_filter = ('ativa',)
    search_fields = ('titulo',)


@admin.register(Ganhador)
class GanhadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'promocao', 'data_inicio_semana', 'ativo')
    list_editable = ('ativo',)
    list_filter = ('promocao', 'ativo', 'data_inicio_semana')
    search_fields = ('nome',)

    fieldsets = (
        ('DADOS DO GANHADOR', {'fields': ('nome', 'foto')}),
        ('PROMOÇÃO E PERÍODO', {'fields': ('promocao', 'data_inicio_semana', 'data_fim_semana')}),
        ('VISIBILIDADE', {'fields': ('ativo',)}),
    )


@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dia_semana', 'horario_inicio', 'horario_fim', 'locutor', 'locutor_substituto')
    list_filter = ('dia_semana', 'locutor')
    search_fields = ('nome',)
    ordering = ('dia_semana', 'horario_inicio')
    
    fieldsets = (
        ('DADOS DO PROGRAMA', {'fields': ('nome', 'dia_semana', 'horario_inicio', 'horario_fim', 'imagem_banner')}),
        ('APRESENTADORES', {
            'fields': ('locutor', 'locutor_substituto'),
            'description': 'Use o Locutor Substituto temporariamente quando alguém estiver cobrindo o horário.'
        }),
    )
