from os import path
from django.urls import path
from django.views.generic import TemplateView
from pedido import views

urlpatterns = [
path('manifestar_interesse/<int:id_disponibilidade>/', views.manifestar_interesse, name='manifestar_interesse'),
path('consultar_meuspedidos/', views.consultar_meuspedidos, name='consultar_meuspedidos'),
path('cancelar_pedido/<int:id_pedido>/', views.cancelar_pedido, name='cancelar_pedido'),
path('desistir_pedido/<int:id_pedido>/', views.desistir_pedido, name='desistir_pedido'),
path('consultar_proprietario/<int:id_pedido>/', views.consultar_proprietario, name='consultar_proprietario'),
]