from django import forms
from django.db import models

from .models import Usuario

class BuscaUsuarioForm(forms.Form):    
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS_USUARIOS = (
        (None, '-----'),
        ('ADMINISTRADOR', 'Administrador'),
        ('COORDENADOR', 'Coordenador' ),
        ('MEMBRO', 'Membro'),
    )
   
    tipo = forms.ChoiceField(label='Tipo de usuário', choices=TIPOS_USUARIOS, required=False)
    
    