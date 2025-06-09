*** Settings ***
Library    RPA.HTTP
Library    RPA.FileSystem

*** Tasks ***
Coletar Documento de Teste
    Create Directory    output
    Download    https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf    target_file=../../uploads/despachos/documento5.pdf
    Log    Documento salvo com sucesso.
