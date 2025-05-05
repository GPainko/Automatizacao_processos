from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


from utils.gerador_hash import gerar_hash

class TipoBeneficioAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class TipoBeneficio(models.Model):       
    titulo = models.CharField('Título do beneficio *', unique=True, db_index=True, max_length=100, help_text='* Campo obrigatório')
    descricao = models.CharField('Descrição do beneficio *', max_length=500, help_text='* Campo obrigatório')
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o tipo de benefício pode ser usado no sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    tipos_beneficios_ativos = TipoBeneficioAtivoManager()

    class Meta:
        ordering            =   ['-is_active','titulo']
        verbose_name        =   'tipo'
        verbose_name_plural =   'tipos'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
        
        self.titulo = self.titulo.upper()           
        super(TipoBeneficio, self).save(*args, **kwargs)
        

    @property
    def get_absolute_url(self):
        return reverse('tipo_beneficio_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('tipo_beneficio_delete', kwargs={'slug': self.slug})
