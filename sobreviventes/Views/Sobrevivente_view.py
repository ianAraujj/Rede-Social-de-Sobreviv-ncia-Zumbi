# rest_framework

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import MethodNotAllowed

# app: sobreviventes
from sobreviventes.models import Localidade, Itens, Sobrevivente, RelatoContaminacao, Recurso
from sobreviventes.serializers import UsuarioSerializer, LocalidadeSerializer, ItemSerializer, SobreviventeSerializer, RecursoSerializer
from sobreviventes.utilitarios import encontrar_localidade, cadastrar_sobrevivente, localizar_sobrevivente, adicionar_recursos

class SobreviventeViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    http_method_names = ['post', 'put', 'get']
    queryset = Sobrevivente.objects.all()
    serializer_class = SobreviventeSerializer


    def create(self, request):

        dados_usuario = {
            "username": self.request.data.get('username', None),
            "password": self.request.data.get('password', None)
        }

        serializer_usuario = UsuarioSerializer(data=dados_usuario)

        if not serializer_usuario.is_valid():
            erros = serializer_usuario.errors
            return Response(
                data={"detalhes": erros},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            latitude = self.request.data['ultimo_local']['latitude']
            longitude = self.request.data['ultimo_local']['longitude']
        except:
            latitude = None
            longitude = None

        localidade = encontrar_localidade(latitude, longitude)

        if localidade == None:

            dados_localizacao = {
                "latitude": latitude,
                "longitude": longitude
            }

            serializer_localidade = LocalidadeSerializer(data=dados_localizacao)

            if not serializer_localidade.is_valid():
                erros = serializer_localidade.errors
                return Response(
                    data={"detalhes": erros},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            localidade = serializer_localidade.save()
    

        dados_sobreviventes = {
            "nome": self.request.data.get("nome", None),
            "idade": self.request.data.get("idade", None),
            "sexo": self.request.data.get("sexo", None),
        }

        serializer_sobrevivente = SobreviventeSerializer(data=dados_sobreviventes)

        if not serializer_sobrevivente.is_valid():
            erros = serializer_sobrevivente.errors
            return Response(
                data={"detalhes": erros},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usuario = serializer_usuario.save()
            novo_sobrevivente = cadastrar_sobrevivente(
                serializer_sobrevivente.validated_data,
                usuario,
                localidade
            )
        except:
            return Response(
                data={"detalhes": "Servidor Indisponível"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        recursos = self.request.data.get('recursos', None)
        adicionar_recursos(novo_sobrevivente, recursos)

        return Response(
            data={"detalhes": "Sobrevivente Cadastrado com Sucesso"}, 
            status=status.HTTP_201_CREATED
        )
        
    def update(self, request):

        sobrevivente = localizar_sobrevivente(request.user)

        if sobrevivente == None:
            return Response(
                data={"detalhes": "Token de Autenticação Não Encontrado."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        localidade_serializer = LocalidadeSerializer(data=request.data)

        if not localidade_serializer.is_valid():
            erros = localidade_serializer.errors
            return Response(
                data = {"detalhes": erros},
                status=status.HTTP_400_BAD_REQUEST
            )

        localidade = encontrar_localidade(
            localidade_serializer.validated_data['latitude'],
            localidade_serializer.validated_data['longitude']
        )

        if localidade == None:
            localidade = Localidade.objects.create(
                latitude = localidade_serializer.validated_data['latitude'],
                longitude = localidade_serializer.validated_data['longitude']
            )
        
        sobrevivente.ultimo_local = localidade
        sobrevivente.save()

        return Response(
            data={"detalhes": "Localização Atualizada com Sucesso"}, 
            status=status.HTTP_200_OK
        )