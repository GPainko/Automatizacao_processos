from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import TipoBeneficio

from .forms import BuscaTipoBeneficioForm


class TipoBeneficioListView(LoginRequiredMixin, ListView):
    model = TipoBeneficio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaTipoBeneficioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaTipoBeneficioForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaTipoBeneficioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaTipoBeneficioForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(descricao__icontains=pesquisa) or Q(titulo__icontains=pesquisa))
            
        return qs
 

class TipoBeneficioCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = TipoBeneficio
    fields = ['titulo', 'descricao', 'is_active']
    success_url = 'tipo_beneficio_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Tipo de benefício cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class TipoBeneficioUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = TipoBeneficio
    fields = ['titulo', 'descricao', 'is_active']
    success_url = 'tipo_beneficio_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Tipo de benefício atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 
    
    
class TipoBeneficioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = TipoBeneficio
    success_url = 'tipo_beneficio_list'

    def get_success_url(self):
        messages.success(self.request, 'Tipo de benefício removido com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à esse tipo de benefício, permissão negada!')
        return redirect(self.success_url)