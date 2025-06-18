*** Settings ***
Library    RPA.HTTP
Library    RPA.FileSystem
Library    DateTime

*** Tasks ***
Coletar Documento de Teste
    # Garante que a pasta de destino existe
    Create Directory    ../../uploads/despachos

    # Gera timestamp para renomear o arquivo
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${new_name}=     Set Variable        despacho_${timestamp}.pdf

    # Faz o download e salva já com o nome personalizado
    Download    https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf 
    ...         target_file=../../uploads/despachos/${new_name}

    Log    Documento salvo como “${new_name}”
