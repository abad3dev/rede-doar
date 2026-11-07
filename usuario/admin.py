from django.contrib import admin

from disponibilidade.models import Disponibilidade
from material.models import Material, TipoMaterial
from pedido.models import Pedido

# Register your models here.

from .models import Estado, Cidade, Usuario

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Usuario)
admin.site.register(Material)
admin.site.register(TipoMaterial)
admin.site.register(Disponibilidade)
admin.site.register(Pedido)
