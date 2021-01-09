from django.db import models
from django.contrib.auth.models import User

class Localidade(models.Model):
    
    latitude = models.CharField(
        verbose_name="Latitude",
        max_length=200,
        blank=False,
        null=False
    )
    
    longitude = models.CharField(
        verbose_name="Longitude",
        max_length=200,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.latitude + " - " + self.longitude


class Itens(models.Model):

    nome = models.CharField(
        verbose_name="Nome do Item",
        max_length=200,
        blank=False,
        null=False,
        unique=True
    )

    pontos = models.IntegerField(
        verbose_name="Pontos",
        blank=False,
        null=False
    )

    def __str__(self):
        return "Nome: " + self.nome + " - Pontos: " + str(self.pontos)

    class Meta:
        verbose_name="Item"
        verbose_name_plural="Itens"

class Sobrevivente(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='usuario_sobrevivente',
        blank=False,
        null=False
    )

    sexo_opcoes = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino')
    )
    
    nome = models.CharField(
        verbose_name="Nome do Sobrevivente",
        max_length=200,
        blank=False,
        null=False
    )

    idade = models.IntegerField(
        verbose_name="Idade",
        blank=False,
        null=False
    )

    sexo = models.CharField(
        verbose_name="Sexo",
        max_length=50,
        choices=sexo_opcoes,
        blank=False,
        null=False
    )

    infectado = models.BooleanField(
        verbose_name="Infectado ou Nao",
        default=False
    )

    ultimo_local = models.ForeignKey(
        Localidade,
        on_delete=models.CASCADE,
        related_name='ultimo_local',
        null=False,
        blank=False
    )

    def __str__(self):
        return self.nome

class Recurso(models.Model):

    item = models.ForeignKey(
        Itens,
        on_delete=models.CASCADE,
        related_name='item',
        null=False,
        blank=False
    )

    quantidade = models.IntegerField(
        verbose_name="Quantidade",
        null=False,
        blank=False
    )

    sobrevivente = models.ForeignKey(
        Sobrevivente,
        on_delete=models.CASCADE,
        related_name='sobrevivente',
        null=False,
        blank=False
    )

    def __str__(self):
        return (
            self.item.nome + ", pontos: " + str(self.item.pontos) + 
            " /// Quantidade: " + str(self.quantidade) + " /// Dono:  " + self.sobrevivente.nome
        )
    

class RelatoContaminacao(models.Model):

    relatado_por = models.ForeignKey(
        Sobrevivente,
        on_delete=models.CASCADE,
        related_name='relatado_por',
        null=False,
        blank=False
    )

    possivel_infectado = models.ForeignKey(
        Sobrevivente,
        on_delete=models.CASCADE,
        related_name='possivel_infectado',
        null=False,
        blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['relatado_por', 'possivel_infectado'], 
            name='Restrição')
        ]
    

    def __str__(self):
        return "Relatado por: " + self.relatado_por.nome + " - Possivel Infectado: " + self.possivel_infectado.nome

