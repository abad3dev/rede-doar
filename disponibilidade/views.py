import re
import requests
from requests.exceptions import RequestException
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from disponibilidade.forms import DisponibilidadeForm
from disponibilidade.models import Disponibilidade
from material.models import Material
from usuario.models import Usuario
from django.contrib.auth.decorators import login_required
from django.db.models import F

# Create your views here.
@login_required
def disponibilizar(request, id_material):
    id_usuario = request.user.id

    if request.method == 'POST':
        form = DisponibilidadeForm(request.POST, request.FILES)

        if form.is_valid():
            nova_disponibilidade = form.save(commit=False)
            nova_disponibilidade.id_usuario_id = id_usuario
            nova_disponibilidade.id_material_id = id_material

            # Busca o cep do usuário
            usuario = get_object_or_404(Usuario, pk=id_usuario)

            if usuario.cep:
                
                cep_limpo = re.sub(r'\D', '', str(usuario.cep))

                if len(cep_limpo) == 8:
                    try:
                        
                        url = f'https://brasilapi.com.br/api/cep/v2/{cep_limpo}'
                        resposta = requests.get(url, timeout=5)

                        if resposta.status_code == 200:
                            dados = resposta.json()
                            location = dados.get('location', {})
                            coordinates = location.get('coordinates', {})

                            lat = coordinates.get('latitude')
                            lng = coordinates.get('longitude')

                            if lat is not None and lng is not None:
                                nova_disponibilidade.latitude = lat
                                nova_disponibilidade.longitude = lng
                    except requests.RequestException:
                        
                        pass

            
            nova_disponibilidade.save()

            messages.success(request, 'Material cadastrado com sucesso!')
            return redirect('iniciar')
        else:
            print('Erros do formulário:', form.errors)
            messages.error(
                request, 'Erro ao cadastrar. Verifique os dados e tente novamente.'
            )

            quantidades = range(1, 1001)
            material_selecionado = get_object_or_404(
                Material, id_material=id_material
            )
            materiais = Material.objects.all()

            return render(
                request,
                'disponibilizar_material.html',
                {
                    'form': form,
                    'id_material': id_material,
                    'material_selecionado': material_selecionado,
                    'quantidades': quantidades,
                    'materiais': materiais,
                    'id_usuario': id_usuario,
                },
            )

    else:
        form = DisponibilidadeForm()
        quantidades = range(1, 1001)
        material_selecionado = get_object_or_404(Material, id_material=id_material)
        materiais = Material.objects.all()

        return render(
            request,
            'disponibilizar_material.html',
            {
                'form': form,
                'id_material': id_material,
                'material_selecionado': material_selecionado,
                'quantidades': quantidades,
                'materiais': materiais,
                'id_usuario': id_usuario,
            },
        )

@login_required
def consultar_meusitens(request):

  id_usuario = request.user.id

  print("ID do usuário:", id_usuario)

  disponibilidades = Disponibilidade.objects.filter(id_usuario=id_usuario).select_related('id_material')

  return render(request, 'consultar_meusitens.html', {'disponibilidades': disponibilidades})


@login_required
def consultar_itensdisponiveis(request):

    id_usuario = request.user.id

    disponibilidades = Disponibilidade.objects.exclude(id_usuario=id_usuario).select_related('id_material')

    return render(request, 'consultar_itensdisponiveis.html', {'disponibilidades': disponibilidades})

@login_required
def excluir_disponibilidade(request, id_disponibilidade):
    
    disponibilidade = get_object_or_404(Disponibilidade, pk=id_disponibilidade)

    if request.method == 'POST':
        disponibilidade.delete()
        return redirect('consultar_meusitens')
        
    return render(request, 'confirmar_exclusao_disponibilidade.html', {'disponibilidade': disponibilidade})

@login_required
def consultar_disponibilidade(request, id_disponibilidade):
    disponibilidade = get_object_or_404(
        Disponibilidade.objects.select_related('id_material', 'id_usuario'),
        id_disponibilidade=id_disponibilidade
    )

    return render(
        request, 
        'mostrar_mapa.html', 
        {'disponibilidade': disponibilidade}
    )