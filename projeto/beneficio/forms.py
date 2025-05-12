from django import forms


class BuscaBeneficioForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    