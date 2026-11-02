
from os import path
from django.urls import path
from django.views.generic import TemplateView
from disponibilidade import views

urlpatterns = [
   path('disponibilizar/<int:id_material>/', views.disponibilizar, name='disponibilizar'),
   path('consultar_minhasdoacoes/', views.consultar_minhasdoacoes, name='consultar_minhasdoacoes'),
   path('consultar_todasdoacoes/', views.consultar_todasdoacoes, name='consultar_todasdoacoes'),

]