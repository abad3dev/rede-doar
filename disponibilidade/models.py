from django.db import models


from material.models import Material
from usuario.models import Usuario


# Create your models here.
class Disponibilidade(models.Model):

    opcoes = [
    ('novo', 'Novo'),
    ('otimo', 'Ótimo'),
    ('bom', 'Bom'),
    ('regular', 'Regular'),
    ('ruim', 'Ruim'),
    ]
    
    id_disponibilidade = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_publicacao = models.DateField(auto_now_add=True)
    arquivo = models.FileField(upload_to='disponibilidade/arquivos/', null=True, blank=True)
    estado_bem = models.CharField(
        max_length=10, 
        choices=opcoes, 
        default='bom'
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )


    def __str__(self):
        return f"{self.id_usuario.nome} - {self.id_material.descricao} - {self.quantidade}"