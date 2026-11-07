from django import forms
from pedido.models import Pedido

class PedidoForm(forms.ModelForm): 
    class Meta:
        model = Pedido
        fields = ['id_disponibilidade']