from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login

from django.shortcuts import redirect
from django.urls import reverse

from django.views.generic import ListView, TemplateView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mail_templated import EmailMessage

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, CoordenadorRequiredMixin

from .models import Usuario
from .forms import BuscaUsuarioForm
from .forms import UsuarioRegisterForm


class UsuarioListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaUsuarioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaUsuarioForm()
        return context

    def get_queryset(self):                
        if (not self.request.user.tipo == 'ADMINISTRADOR'):
            qs = super().get_queryset().exclude(tipo = 'ADMINISTRADOR')
        else:
            qs = super().get_queryset().all()
        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaUsuarioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaUsuarioForm()

        if form.is_valid():            
            tipo = form.cleaned_data.get('tipo')
                        
            if tipo:
                qs = qs.filter(tipo=tipo)
            
        return qs


class UsuarioCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Usuario
    fields = ['tipo', 'nome', 'instituicao', 'cpf', 'email', 'password', 'is_active']
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Usuário cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class UsuarioUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Usuario
    fields = ['tipo', 'nome', 'instituicao', 'cpf', 'email', 'is_active']
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados do usuário atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class UsuarioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Usuario
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Usuário removido com sucesso da plataforma!')
        return reverse(self.success_url)


    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """        
        try:
            self.get_object().delete()
        except Exception as e:
            messages.error(request, f'Há dependências ligadas a esse Usuário, permissão negada! Erro: {e}')
        return redirect(self.success_url)

