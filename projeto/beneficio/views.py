from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import Beneficio

from .forms import BuscaBeneficioForm


class BeneficioListView(LoginRequiredMixin, ListView):
    model = Beneficio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaBeneficioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaBeneficioForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaBeneficioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaBeneficioForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(descricao__icontains=pesquisa) or Q(titulo__icontains=pesquisa))
            
        return qs
 

class BeneficioCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Beneficio
    fields = [
    'numero_beneficio',
    'servidor',
    'tipo_beneficio',
    'nome_beneficiario',
    'cpf',
    'email',
    'estado',
    'cidade',
    'bairro',
    'rua',
    'numero_residencia',
    'complemento_residencia',
    'is_active',
]
    success_url = 'beneficio_list'
    
    def get_success_url(self):
        messages.success(self.request, 'benefício cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class BeneficioUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Beneficio
    fields = [
    'numero_beneficio',
    'servidor',
    'tipo_beneficio',
    'nome_beneficiario',
    'cpf',
    'email',
    'estado',
    'cidade',
    'bairro',
    'rua',
    'numero_residencia',
    'complemento_residencia',
    'is_active',
]
    success_url = 'beneficio_list'
    
    def get_success_url(self):
        messages.success(self.request, 'benefício atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 
    
    
class BeneficioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Beneficio
    success_url = 'beneficio_list'

    def get_success_url(self):
        messages.success(self.request, 'benefício removido com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à esse benefício, permissão negada!')
        return redirect(self.success_url)