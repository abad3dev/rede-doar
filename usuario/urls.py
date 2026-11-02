from django.urls import path
from usuario import views

urlpatterns = [
    # Aqui nós chamamos a sua função "cadastrar_usuario" que está no views.py
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('mostrar_cadastro/', views.mostrar_cadastro, name='mostrar_cadastro'),
    path('', views.iniciar, name='iniciar'),
]