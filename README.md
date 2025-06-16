# Automatização de Processos no INSS


Este projeto foca na automatização e padronização de processos administrativos por meio de robôs de software, especialmente Robotic Process Automation (RPA), que executam tarefas repetitivas e propensas a erros humanos em sistemas informatizados. O contexto de aplicação envolve processos do Instituto Nacional do Seguro Social (INSS), que incluem subprocessos manuais de análise e despacho de benefícios, como aposentadorias, auxílios e pensões. Esses subprocessos são atualmente realizados por funcionários servidores e estão sujeitos a falhas. A proposta justifica-se pela necessidade de reduzir erros e tornar o fluxo mais eficiente, eliminando atividades manuais repetitivas. O objetivo é projetar e implementar um sistema que automatize e padronize as tarefas de despacho e notificação aos segurados, melhorando a gestão de benefícios do INSS.

## apps
    - (OK)usuário
        - (OK)tipo
        - (OK)nome
        - (OK)aps
        - (OK)email
        - (OK)cpf
        - (OK)is_active
        - (OK)slug

    - (OK) instituicao/aps
        - (OK)nome
        - (OK)sigla
        - (OK)estado
        - (OK)cidade
        - (OK)is_active
        - (OK)slug

    - aviso
        - titulo
        - texto
        - arquivo
        - destinatário - beneficiado sobre irregularidade - referencia benefício
        - destinatário comprovação - funcionário ou email do setor - referencia usuario coordenação ou setor
        - data e hora
        - is_active
        - slug

    - (OK)tipo benefício
        - (OK)titulo
        - (OK)descricao
        - (OK)is_active
        - (OK)slug        

    - (OK)beneficio em irregularidade/análise
        - (OK)número do benefício
        - (OK)servidor delegado para análise referencia Usuario
        - (OK)tipoBeneficio referencia TipoBeneficio
        - (OK)nome beneficiário
        - (OK)cpf
        - (OK)email
        - (OK)cep
        - (OK)estado
        - (OK)cidade
        - (OK)bairro
        - (OK)rua
        - (OK)número
        - (OK)complemento
        - (OK)is_active
        - (OK)slug    

    - despacho
        - beneficio referencia beneficio
        - texto gerado
        - documentação selecionada (lista) referencia documentacao 
        - documento de notificação pdf (gerado dinamicamente)
        - enviado por email? (boolean)
        - gerar envelope para enviado por correios (boolean)
        -

    - documentacao benefício em irregularidade
        - benefício referencia benefício
        - descricao
        - arquivo documento
        - is_active
        - slug

# .env
```
SECRET_KEY='-2tj8*6+h1bgh6(3+4mcc2nl0@57!c*1xhu*p@-(180qm_#(a('
DEBUG=True
STATIC_URL=/static/
DOMINIO_URL='localhost:8000'
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_USE_STARTTLS = False
```


# Usando o ReportLab do Python-Django

## Instalar o pacote reportlab
```
    pip install reportlab==4.2.2
``` 

## Criar um DespachoPdfView dentro da view.py do app despacho

### Importar os pacotes 
```
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.lib.units import inch
    from reportlab.lib import colors
``` 

### Implementar a view - LEMBRAR de onde tem inscricao é o depacho

```
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
        evento_titulo = getattr(inscricao.evento, 'titulo', inscricao.evento.nome)  # Usar titulo se existir, senão nome
        
        # Formatação das datas e horários
        data_inicio = inscricao.evento.data_inicio.strftime('%d/%m/%Y') if inscricao.evento.data_inicio else 'N/A'
        hora_inicio = getattr(inscricao.evento, 'hora_inicio', None)
        hora_inicio_str = hora_inicio.strftime('%H:%M') if hora_inicio else 'N/A'

        texto_atestado = f"""
        Atestamos que <b>{inscricao.participante.nome}</b> participou do evento <b>{evento_titulo}</b>, 
        realizado no dia <b>{data_inicio}</b>, às <b>{hora_inicio_str}</b> horas, 
        no local <b>{inscricao.evento.local}</b>, situado em <b>{inscricao.evento.instituicao}</b>. 
        O referido evento teve carga horária total de <b>{ inscricao.evento.carga_horaria }</b> 
        hora(s) e foi promovido e coordenado pelo(a) <b>{ inscricao.evento.grupo }</b>.
        <br/>
        O código de inscrição para validação do atestado é <b>{ inscricao.codigo_matricula }</b>.
        """
        
        story.append(Paragraph(texto_atestado, justify_style))
        story.append(Spacer(1, 40))

        data_texto = f"Santa Maria, { inscricao.evento.data_inicio.strftime('%d de %B de %Y')}."
        story.append(Paragraph(data_texto, right_style))
        story.append(Spacer(1, 50))
        
        # Texto final explicativo
        texto_final = """
        <i>O atestado de participação é gerado automaticamente pelo Sistema de Gestão de Eventos (SGEUFN), 
        no momento em que o participante confirma sua presença no evento. Para validar a autenticidade
        deste atestado, utilize o código de inscrição fornecido acima no formulário de validação do SGEUFN.</i>
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

```

### Adicionar na url.py do app despacho

```
from .views import DespachoPdfView


path('despacho/<slug:slug>/pdf/', DespachoPdfView.as_view(), name='despacho_pdf'),

```

### Adicionar no template despacho_list.html

```
<th class="text-center">Arquivo despacho</th>


<td class="text-center">  							
    <span data-toggle="tooltip" title="Imprimir PDF">
        {% bootstrap_button content='' href=despacho.get_gera_documento_url button_type='link' icon='print' button_class='btn btn-success' size='sm' %}
    </span>
        
</td>

```

### Adcionar a property get_gera_documento_url no models.py do app despacho

```
@property
def get_gera_documento_url(self):
    return reverse('despacho_pdf', kwargs={'slug': self.slug})
```
