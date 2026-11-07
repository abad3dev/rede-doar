from django.db import models



from disponibilidade.models import Disponibilidade
from usuario.models import Usuario


opcoes = [
    ('aceito', 'Aceito'),
    ('desistido', 'Desistido'),
    ('pendente', 'Pendente'),
    ('finalizado', 'Finalizado'),
    ('recusado', 'Recusado'),
]


# Create your models here.
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_disponibilidade = models.ForeignKey(Disponibilidade, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15,
        choices=opcoes,
        default='pendente'
    )
    data_solicitacao = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id_usuario', 'id_disponibilidade'],
                name='unique_pedido_usuario_disponibilidade'
            )
        ]



    def __str__(self):
        return f"Pedido {self.id_pedido} - Usuário {self.id_usuario_id} - Disponibilidade {self.id_disponibilidade_id}"