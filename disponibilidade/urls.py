
from os import path
from django.urls import path
from django.views.generic import TemplateView
from disponibilidade import views

urlpatterns = [
   path('disponibilizar/<int:id_material>/', views.disponibilizar, name='disponibilizar'),
   path('consultar_meusitens/', views.consultar_meusitens, name='consultar_meusitens'),
   path('consultar_itensdisponiveis/', views.consultar_itensdisponiveis, name='consultar_itensdisponiveis'),
   path('excluir/<int:id_disponibilidade>/', views.excluir_disponibilidade, name='excluir_disponibilidade'),
   path('mostrar_mapa/<int:id_disponibilidade>/', views.consultar_disponibilidade, name='mostrar_mapa'),

]