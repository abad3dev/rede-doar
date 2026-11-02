from urllib import request

from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render

import usuario
from usuario.forms import UsuarioCadastroForm, UsuarioForm
from django.contrib.auth.decorators import login_required

from usuario.models import Cidade, Usuario
from material.models import Material, TipoMaterial

@login_required
def iniciar(request):
    materiais = Material.objects.all()
    tipomateriais = TipoMaterial.objects.all()
    return render(request, 'iniciar.html', {'materiais': materiais})

@login_required
def cadastrar_usuario(request):
    # 1. Proteção: Se o usuário já tem usuário, manda pro sistema e barra a tela de cadastro
    if hasattr(request.user, 'usuario'):
        return redirect('iniciar') 
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
    
            novo_usuario = form.save(commit=False)
    
            novo_usuario.usuario = request.user 
    
            novo_usuario.save()
            
            messages.success(request, 'Usuário cadastrado com sucesso!')
    
            return redirect('iniciar') 
        else:
            print("Erros do formulário:", form.errors)
            messages.error(request, 'Erro ao cadastrar. Verifique os dados e tente novamente.')
    else:
        form = UsuarioForm()

    cidades = Cidade.objects.all().order_by('nome')
       
    return render(request, 'cadastrar_usuario.html', {'form': form, 'cidades': cidades})

@login_required
def mostrar_cadastro(request):

    id_usuario = request.user.id

    usuario = get_object_or_404(Usuario, pk=id_usuario)

    cidades = Cidade.objects.all().order_by('nome')

    if request.method == 'POST':

        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro atualizado com sucesso!')

        else:
            print("Erros do formulário:", form.errors)
            messages.error(request, 'Erro ao cadastrar. Verifique os dados e tente novamente.')

        
        
        return redirect('mostrar_cadastro')
        
    return render(request, 'mostrar_cadastro.html', {'usuario': usuario, 'cidades': cidades})

    
