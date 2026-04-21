from django.db import models
from django.templatetags.static import static

class Locutor(models.Model):
    """
    Model para representar os locutores/profissionais da rádio.
    """
    nome = models.CharField('Nome do Locutor', max_length=100)
    foto = models.ImageField('Foto do Locutor', upload_to='locutores/', blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Locutor'
        verbose_name_plural = 'Locutores'

class Promocao(models.Model):
    """
    Gerencia as promoções ativas que aparecem no carrossel do site.
    Cada promoção pode ter um link direto para o WhatsApp já com mensagem pronta.
    """
    titulo = models.CharField('Título da Promoção', max_length=150)
    descricao = models.TextField('Descrição', blank=True, null=True)
    imagem_banner = models.ImageField('Banner da Promoção', upload_to='promocoes/', blank=True, null=True)
    link_whatsapp = models.URLField(
        'Link de Redirecionamento (WhatsApp)', 
        blank=True, null=True, 
        help_text="Ex: https://wa.me/5534996491118?text=Quero+Participar"
    )
    ativa = models.BooleanField('Promoção Ativa?', default=True)
    criada_em = models.DateTimeField('Criada em', auto_now_add=True)

    def __str__(self):
        return self.titulo

        
    class Meta:
        verbose_name = 'Promoção'
        verbose_name_plural = 'Promoções'
        ordering = ['-criada_em']


class Ganhador(models.Model):
    """
    Model para gerenciar os ganhadores da semana.
    Exibidos em destaque abaixo do carrossel.
    """
    nome = models.CharField('Nome do Ganhador', max_length=100)
    foto = models.ImageField(
        'Foto do Ganhador', 
        upload_to='ganhadores/', 
        help_text="Importante: Use fotos no formato 4:5 (Instagram Post) para melhor visualização."
    )

    promocao = models.ForeignKey(
        Promocao, on_delete=models.CASCADE, 
        related_name='ganhadores', 
        verbose_name='Promoção Associada'
    )
    data_inicio_semana = models.DateField('Início da Semana')
    data_fim_semana = models.DateField('Fim da Semana')
    ativo = models.BooleanField('Exibir no Site?', default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.promocao.titulo}"

    class Meta:
        verbose_name = 'Ganhador'
        verbose_name_plural = 'Ganhadores'
        ordering = ['-data_inicio_semana', '-criado_em']


class Programa(models.Model):
    """
    Representa o programa da grade de programação da rádio Central FM.
    Controla automaticamente o que é exibido no site "No Ar Agora".
    """
    DIAS_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    nome = models.CharField('Nome do Programa', max_length=150)
    dia_semana = models.CharField('Dia da Semana', max_length=10, choices=DIAS_SEMANA)
    horario_inicio = models.TimeField('Horário de Início')
    horario_fim = models.TimeField('Horário de Término')
    locutor = models.ForeignKey(
        Locutor, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='programas',
        help_text="Quem está apresentando este programa?"
    )
    imagem_banner = models.ImageField(
        'Banner do Programa', upload_to='programas/banners/', 
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.nome} ({self.get_dia_semana_display()})"

    class Meta:
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
        ordering = ['dia_semana', 'horario_inicio']
