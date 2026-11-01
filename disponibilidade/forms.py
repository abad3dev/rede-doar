from django import forms
from disponibilidade.models import Disponibilidade


class DisponibilidadeForm(forms.ModelForm): 
    class Meta:
        model = Disponibilidade
        fields = ['quantidade', 'valor_estimado', 'arquivo']

