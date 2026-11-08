from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from urllib3 import request
from pedido.forms import PedidoForm
from .models import Pedido
from django.contrib.auth.models import User

# Create your views here.
@login_required
def manifestar_interesse(request, id_disponibilidade):
    id_usuario = request.user.id

    # Verifica se já existe um pedido para esse usuário e essa disponibilidade
    ja_existe = Pedido.objects.filter(
        id_usuario_id=id_usuario,
        id_disponibilidade_id=id_disponibilidade
    ).exists()

    if ja_existe:
        messages.warning(request, 'Você já manifestou interesse neste item.')
        return redirect('consultar_itensdisponiveis')

    if request.method == 'POST':
        form = PedidoForm(request.POST)

        if form.is_valid():
            novo_pedido = form.save(commit=False)
            novo_pedido.id_usuario_id = id_usuario
            novo_pedido.id_disponibilidade_id = id_disponibilidade
            novo_pedido.save()

            messages.success(request, 'Pedido cadastrado com sucesso!')
            return redirect('consultar_itensdisponiveis')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os dados e tente novamente.')
    else:
        form = PedidoForm()

    return render(request, 'confirmar_pedido.html', {
        'form': form,
        'id_disponibilidade': id_disponibilidade,
    })


@login_required
def consultar_solicitacoes(request):
    id_usuario = request.user.id

    pedidos = Pedido.objects.filter(
        id_disponibilidade__id_usuario_id=id_usuario
    ).select_related(
        'id_usuario',  # Carrega os dados do solicitante do pedido
        'id_disponibilidade',
        'id_disponibilidade__id_material'
    )

    return render(request, 'consultar_solicitacoes.html', {'pedidos': pedidos})

@login_required
def consultar_meuspedidos(request):
    id_usuario = request.user.id

    pedidos = Pedido.objects.filter(
        id_usuario_id=id_usuario
    ).select_related(
        'id_disponibilidade', 
        'id_disponibilidade__id_material'
    )

    return render(request, 'consultar_meuspedidos.html', {'pedidos': pedidos})

@login_required
def consultar_proprietario(request, id_pedido):
    pedido = get_object_or_404(
        Pedido.objects.select_related(
            'id_disponibilidade__id_usuario',
            'id_disponibilidade__id_material',
        ),
        pk=id_pedido,
    )

    proprietario = pedido.id_disponibilidade.id_usuario

    user_auth = User.objects.filter(username=proprietario.usuario).first()
    email_proprietario = user_auth.email if user_auth else None

    return render(
        request,
        'consultar_proprietario.html',
        {
            'pedido': pedido,
            'proprietario': proprietario,
            'email_proprietario': email_proprietario,
        },
    )

@login_required
def consultar_solicitante(request, id_pedido):
    
    pedido = get_object_or_404(
        Pedido.objects.select_related(
            'id_usuario',  
            'id_disponibilidade__id_material',
        ),
        pk=id_pedido,
    )

    
    solicitante = pedido.id_usuario

    
    user_auth = User.objects.filter(username=solicitante.usuario).first()
    email_solicitante = user_auth.email if user_auth else None

    return render(
        request,
        'consultar_solicitante.html',  
        {
            'pedido': pedido,
            'solicitante': solicitante,
            'email_solicitante': email_solicitante,
        },
    )

@login_required
def cancelar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)

    if request.method == 'POST':
        pedido.status = 'cancelado'
        pedido.save()
        messages.success(request, 'Pedido cancelado com sucesso!')
        return redirect('consultar_meuspedidos')
        
    return render(request, 'confirmar_cancelamento.html', {'pedido': pedido})

@login_required
def desistir_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)

    if request.method == 'POST':
        pedido.status = 'desistido'
        pedido.save()
        messages.success(request, 'Pedido desistido com sucesso!')
        return redirect('consultar_meuspedidos')
        
    return render(request, 'confirmar_desistencia.html', {'pedido': pedido})

@login_required
def aceitar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)

    if request.method == 'POST':
        pedido.status = 'aceito'
        pedido.save()
        messages.success(request, 'Pedido aceito com sucesso!')
        return redirect('consultar_solicitacoes')
        
    return render(request, 'aceitar_pedido.html', {'pedido': pedido})

@login_required
def recusar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)

    if request.method == 'POST':
        pedido.status = 'recusado'
        pedido.save()
        messages.success(request, 'Pedido recusado com sucesso!')
        return redirect('consultar_solicitacoes')
        
    return render(request, 'recusar_pedido.html', {'pedido': pedido})