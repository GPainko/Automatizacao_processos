from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


from utils.gerador_hash import gerar_hash
from usuario.models import Usuario
from tipo_beneficio.models import TipoBeneficio

class BeneficioAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Beneficio(models.Model):       
    numero_beneficio = models.CharField('Número do beneficio *', unique=True, db_index=True, max_length=100, help_text='* Campo obrigatório')
    servidor = models.ForeignKey(
        'usuario.Usuario',              # ou 'usuario.Usuario'
        verbose_name='Servidor delegado *',
        on_delete=models.PROTECT,
        related_name='beneficios',             # nome pythonico, sem espaços
    )
    tipo_beneficio = models.ForeignKey(
        'tipo_beneficio.TipoBeneficio',        # app_label.ModelName
        verbose_name='Tipo de Benefício *',
        on_delete=models.PROTECT,
        related_name='beneficios',             # sem espaços
    )
    nome_beneficiario = models.CharField('Nome completo *', max_length=100)
    cpf = models.CharField('CPF *', max_length=14, help_text='ATENÇÃO: Somente os NÚMEROS')
    email = models.EmailField('Email', unique=True, max_length=100, db_index=True)
    estado = models.CharField('Estado ou província *', max_length=30)
    cidade = models.CharField('Cidade', max_length=100, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=100, null=True, blank=True)
    rua = models.CharField('Rua', max_length=100, null=True, blank=True)
    numero_residencia = models.CharField('Número', max_length=100, null=True, blank=True)
    complemento_residencia = models.CharField('Complemento', max_length=100, null=True, blank=True)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o tipo de benefício pode ser usado no sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    tipos_beneficios_ativos = BeneficioAtivoManager()

    class Meta:
        ordering            =   ['-is_active','numero_beneficio']
        verbose_name        =   'beneficio'
        verbose_name_plural =   'beneficios'

    def __str__(self):
        return '[%s] %s: %s. CPF: %s' % (self.tipo_beneficio, self.numero_beneficio, self.nome_beneficiario, self.cpf)

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
        
        self.numero_beneficio = self.numero_beneficio.upper()           
        super(Beneficio, self).save(*args, **kwargs)
        

    @property
    def get_absolute_url(self):
        return reverse('beneficio_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('beneficio_delete', kwargs={'slug': self.slug})
