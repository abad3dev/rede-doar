
import re
import requests
from django import forms
from django.core.exceptions import ValidationError
from usuario.models import Usuario


class UsuarioForm(forms.ModelForm): 
    class Meta:
        model = Usuario
        exclude = ['usuario']

class UsuarioCadastroForm(forms.ModelForm): 
    class Meta:
        model = Usuario
        exclude = ['usuario']

  