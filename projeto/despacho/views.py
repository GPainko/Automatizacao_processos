from __future__ import unicode_literals

from django.contrib.staticfiles import finders

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import Despacho

from .forms import BuscaDespachoForm

import subprocess
import os



class DespachoListView(LoginRequiredMixin, ListView):
    model = Despacho

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaDespachoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaDespachoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaDespachoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaDespachoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(beneficio__numero_beneficio__icontains=pesquisa) or Q(benefico__nome_beneficiario__icontains=pesquisa) or 
                Q(benefico__cpf__icontains=pesquisa))
            
        return qs
 

class DespachoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Despacho
    fields = ['beneficio','is_active']
    success_url = 'despacho_list'

    def form_valid(self, form):
        # Etapa 1: Gera texto de despacho automaticamente
        caminho_documento= str(finders.find('despacho/texto_despacho/mensagem.txt'))

        with open(caminho_documento, 'r', encoding='utf-8') as arquivo:
            texto = arquivo.read()

        
        # Etapa 2: Executa robô Sabin via RCC (Robocorp)
        try:
            sabin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../projeto/sabin/"))
            subprocess.run(
                ["rcc", "run"],
                cwd=sabin_path,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print("Erro ao executar robô Sabin:", e)
            # mensagens.warning(self.request, 'Robô Sabin falhou.')

        return super().form_valid(form)

    
    def get_success_url(self):
        messages.success(self.request, 'Despacho cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class DespachoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Despacho
    fields = [
    'texto',
    'is_active',
]
    success_url = 'despacho_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Despacho atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 
    
    
class DespachoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Despacho
    success_url = 'despacho_list'

    def get_success_url(self):
        messages.success(self.request, 'Despacho removido com sucesso na plataforma!')
        return reverse(self.success_url) 

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse despacho, permissão negada!')
        return redirect(self.success_url)