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
from sobreviventes.serializers import RelatoContaminacaoSerializer, LocalidadeSerializer, SobreviventeSerializer, RecursoSerializer
from sobreviventes.utilitarios import localizar_sobrevivente, verificar_limite_relatos
from sobreviventes.validadores import validar_sobrevivente


class RelatoContaminacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    queryset = RelatoContaminacao.objects.all()
    serializer_class = RelatoContaminacaoSerializer

    def create(self, request):

        relatado_por = localizar_sobrevivente(request.user)
        if relatado_por == None:
            return Response(
                data={"detalhes": "Token de Autenticação Inválido."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        infectado_id = self.request.data.get('infectado_id', None)
        valido, erro, codigo_http = validar_sobrevivente(infectado_id)

        if not valido:
            mensagem_erro = {
                "infectado_id": erro
            }
            return Response(
                data={"detalhes": mensagem_erro},
                status=codigo_http
            )
        
        possivel_infectado = Sobrevivente.objects.get(id=infectado_id)

        if RelatoContaminacao.objects.filter(relatado_por=relatado_por, possivel_infectado=possivel_infectado).exists():
            return Response(
                data={"detalhes": "Relato de Contaminação Já Realizado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        RelatoContaminacao.objects.create(
            relatado_por = relatado_por,
            possivel_infectado = possivel_infectado
        )

        infectado = verificar_limite_relatos(possivel_infectado)
        if infectado:
            possivel_infectado.infectado = True
            possivel_infectado.save()


        return Response(
            data={"detalhes": "Sinalização de Infectado Realizada com Sucesso."},
            status=status.HTTP_201_CREATED
        )
