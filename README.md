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

    - beneficio em irregularidade/análise
        - número do benefício
        - servidor delegado para análise referencia Usuario
        - tipoBeneficio referencia TipoBeneficio
        - nome beneficiário
        - cpf
        - email
        - cep
        - estado
        - cidade
        - bairro
        - rua
        - número
        - complemento
        - is_active
        - slug    

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