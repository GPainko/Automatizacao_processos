# Standard library
import os
import subprocess
import locale
import logging

# Django / third-party
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors

# Local app imports
from utils.decorators import LoginRequiredMixin, StaffRequiredMixin
from .models import Despacho
from .forms import BuscaDespachoForm

logger = logging.getLogger(__name__)


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
        # Etapa Executa robô Sabin via RCC (Robocorp)
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

class DespachoPdfView(LoginRequiredMixin, DetailView):
    model = Despacho
    
    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        despacho = self.get_object()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="documento_{despacho.beneficio.tipo_beneficio.titulo}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4, 
                              topMargin=1*inch, bottomMargin=1*inch,
                              leftMargin=1*inch, rightMargin=1*inch)
        story = []
        
        styles = getSampleStyleSheet()

        caminho_imagem_lap = finders.find('core/img/logo_lapinf_hor.png')

        imagem_lap = Image(caminho_imagem_lap, width=220,height=75)
        
        # Estilo do título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=40,
            spaceBefore=40,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para texto justificado
        justify_style = ParagraphStyle(
            'JustifyStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=18
        )
        
        # Estilo para texto centralizado
        center_style = ParagraphStyle(
            'CenterStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )

        right_style = ParagraphStyle(
            'RightStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_RIGHT,
            fontName='Helvetica'
        )
        
        # colocar logo do LAP        
        story.append(imagem_lap)
        
        # Título do documento
        story.append(Paragraph("TITULO DO DOCUMENTO", title_style))
        story.append(Spacer(1, 20))
        
        # Texto principal do atestado
        evento_titulo = getattr(despacho.beneficio.numero_beneficio, 'titulo', despacho.beneficio.tipo_beneficio)  # Usar titulo se existir, senão nome

        texto_atestado = f"""
        O Referente beneficio N° <b>{despacho.beneficio.numero_beneficio}</b> está atualmente em face de analise.
        """
        
        story.append(Paragraph(texto_atestado, justify_style))
        story.append(Spacer(1, 40))

        # data_texto = f"Santa Maria, { inscricao.evento.data_inicio.strftime('%d de %B de %Y')}."
        # story.append(Paragraph(data_texto, right_style))
        # story.append(Spacer(1, 50))
        
        # Texto final explicativo
        texto_final = """
        <i>O segurado tem o data limite de 30 dias para se apresentar a uma aps do INSS .</i>
        """
        
        story.append(Paragraph(texto_final, justify_style))
        story.append(Spacer(1, 40))
        
        # Rodapé com informações do sistema
        story.append(Spacer(1, 20))
        
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique',
            textColor=colors.grey
        )
        
        rodape_texto = f"""
        ___________________________________________________<br/>
        Laboratório de Práticas Computação UFN<br/>
        Rua dos Andradas, 1614 – Santa Maria – RS<br/>
        CEP 97010-032 - https://sge.lapinf.ufn.edu.br
        """
        
        story.append(Paragraph(rodape_texto, footer_style))
        
        # Constrói o PDF
        doc.build(story)
        
        return response
    
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