from django import forms


class BuscaTipoBeneficioForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    