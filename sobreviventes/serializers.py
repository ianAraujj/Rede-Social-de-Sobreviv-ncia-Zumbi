from rest_framework import serializers
from sobreviventes.models import Localidade, Itens, Sobrevivente, RelatoContaminacao, Recurso
from django.contrib.auth.models import User


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = super(UsuarioSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LocalidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Localidade
        fields = "__all__"

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Itens
        fields = "__all__"

class SobreviventeSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    ultimo_local = LocalidadeSerializer(many=False, read_only=True)

    class Meta:
        model = Sobrevivente
        fields = ('id', 'usuario', 'nome', 'idade', 'sexo', 'ultimo_local')
    
class RecursoSerializer(serializers.ModelSerializer):
    sobrevivente = SobreviventeSerializer(many=False, read_only=True)
    item = ItemSerializer(many=False, read_only=True)

    class Meta:
        model = Recurso
        fields = ('sobrevivente', 'item', 'quantidade')

class RelatoContaminacaoSerializer(serializers.ModelSerializer):

    relatado_por = SobreviventeSerializer(many=False, read_only=False)
    possivel_infectado = SobreviventeSerializer(many=False, read_only=False)

    class Meta:
        model = RelatoContaminacao
        fields = ('relatado_por', 'possivel_infectado')