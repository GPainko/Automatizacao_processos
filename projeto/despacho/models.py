from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


from utils.gerador_hash import gerar_hash
from usuario.models import Usuario

from pathlib import Path

class DespachoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Despacho(models.Model):
    # - beneficio referencia beneficio
    #     - texto gerado
    #     - documentação selecionada (lista) referencia documentacao 
    #     - documento de notificação pdf (gerado dinamicamente)
    #     - enviado por email? (boolean)
    #     - gerar envelope para enviado por correios (boolean)       
    beneficio = models.ForeignKey(
        'beneficio.Beneficio',              # ou 'usuario.Usuario'
        verbose_name='Beneficio associado *',
        on_delete=models.PROTECT,
        related_name='beneficio',             # nome pythonico, sem espaços
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    texto = models.TextField('Texto *', max_length=20000)
    arquivo_notificao = models.FileField('Arquivo do texto do despacho *', null=True, blank=True)
    envios_email = models.IntegerField('Quantidade de vezes que o despacho foi notificado por email.', default=0)
    data_ultimo_envio = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o despacho pode ser usado no sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    despachos_ativos = DespachoAtivoManager()

    class Meta:
        ordering            =   ['-is_active', 'data_criacao', 'beneficio']
        verbose_name        =   'despacho'
        verbose_name_plural =   'despachos'

    def __str__(self):
        return '%s | %s' % (self.beneficio, self.data_criacao)

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
                  
        super(Despacho, self).save(*args, **kwargs)
        

    @property
    def get_absolute_url(self):
        return reverse('despacho_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('despacho_delete', kwargs={'slug': self.slug})
    
    @property
    def listar_documentos_encontrados(self):
        pasta = Path("uploads/despachos")
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@', pasta)
        resposta = ''
        for arquivo in pasta.iterdir():
            if arquivo.is_file():
                print(arquivo.name)
                resposta = resposta + arquivo.name + '; '
        return resposta