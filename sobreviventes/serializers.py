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

class RecursoSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, read_only=True)

    class Meta:
        model = Recurso
        fields = ('item', 'quantidade')

class SobreviventeSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    ultimo_local = LocalidadeSerializer(many=False, read_only=True)
    inventario = RecursoSerializer(many=True, read_only=True)

    class Meta:
        model = Sobrevivente
        fields = ('usuario', 'nome', 'idade', 'sexo', 'ultimo_local', 'inventario')
    
    """
    def validate(self, data):
        return data
    """