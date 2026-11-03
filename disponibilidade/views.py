from urllib import request

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from disponibilidade.forms import DisponibilidadeForm
from disponibilidade.models import Disponibilidade
from material.models import Material
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
            'quantidades': quantidades,
            'materiais': materiais,
            'id_usuario': id_usuario,
        },
    )



@login_required
def consultar_meusitens(request):

  id_usuario = request.user.id

  print("ID do usuário:", id_usuario)

  disponibilidades = Disponibilidade.objects.filter(id_usuario=id_usuario).select_related('id_material').annotate(valor_total=F('quantidade') * F('valor_estimado'))

  return render(request, 'consultar_meusitens.html', {'disponibilidades': disponibilidades})


@login_required
def consultar_itensdisponiveis(request):

    id_usuario = request.user.id

    disponibilidades = Disponibilidade.objects.exclude(id_usuario=id_usuario).select_related('id_material').annotate(valor_total=F('quantidade') * F('valor_estimado'))

    return render(request, 'consultar_itensdisponiveis.html', {'disponibilidades': disponibilidades})

@login_required
def excluir_disponibilidade(request, id_disponibilidade):
    
    disponibilidade = get_object_or_404(Disponibilidade, pk=id_disponibilidade)

    if request.method == 'POST':
        disponibilidade.delete()
        return redirect('consultar_meusitens')
        
    return render(request, 'confirmar_exclusao_disponibilidade.html', {'disponibilidade': disponibilidade})
