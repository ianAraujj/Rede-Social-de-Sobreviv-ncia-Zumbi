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
from sobreviventes.models import Itens, Sobrevivente, Recurso
from sobreviventes.serializers import ItemSerializer, SobreviventeSerializer, RecursoSerializer
from sobreviventes.validadores import validar_sobrevivente
from sobreviventes.utilitarios import calcular_igualdade_troca, adicionar_recursos, decrementar_recursos, possui_recurso


class RecursoViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    http_method_names = ['post']
    serializer_class = RecursoSerializer

    def create(self, request):

        try:
            sobrevivente_1 = self.request.data['sobrevivente_1']['id']
        except:
            sobrevivente_1 = None
        try:
            sobrevivente_2 = self.request.data['sobrevivente_2']['id']
        except:
            sobrevivente_2 = None

        valido, erro, codigo_http = validar_sobrevivente(sobrevivente_1)
        if not valido:
            mensagem_erro = {
                "sobrevivente_1": {
                    "id": erro
                }
            }
            return Response(
                data={"detalhes": mensagem_erro},
                status=codigo_http
            )
        valido, erro, codigo_http = validar_sobrevivente(sobrevivente_2)
        if not valido:
            mensagem_erro = {
                "sobrevivente_2": {
                    "id": erro
                }
            }
            return Response(
                data={"detalhes": mensagem_erro},
                status=codigo_http
            )
        
        if sobrevivente_1 == sobrevivente_2:
            return Response(
                data = {"detalhes": "Os sobreviventes informados são iguais."},
                status = status.HTTP_403_FORBIDDEN
            )

        sobrevivente_1_obj = Sobrevivente.objects.get(id=sobrevivente_1)
        sobrevivente_2_obj = Sobrevivente.objects.get(id=sobrevivente_2)

        if sobrevivente_1_obj.infectado or sobrevivente_2_obj.infectado:
            return Response(
                data = {"detalhes": "Os sobreviventes Infectados Não tem Permissão para Realizar Trocas."},
                status = status.HTTP_403_FORBIDDEN
            )

        try:
            recursos_sobrevivente_1 = self.request.data['sobrevivente_1']['recursos']
            recursos_sobrevivente_2 = self.request.data['sobrevivente_2']['recursos']
        except:
            recursos_sobrevivente_1 = None
            recursos_sobrevivente_2 = None
        
        dados_invalidos, igualdade = calcular_igualdade_troca(
            recursos_sobrevivente_1,
            recursos_sobrevivente_2
        )

        if dados_invalidos:
            erro = "Este campo é obrigatório. Deve ser um array contendo os campos: 'item' (nome do item) e 'quantidade'."
            mensagem_erro = {
                "recursos": erro
            }
            return Response(
                data = {"detalhes": mensagem_erro},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if not igualdade:
            return Response(
                data = {"detalhes": "Não há uma Igualdade de Pontos para Realizar a Troca"},
                status = status.HTTP_400_BAD_REQUEST
            )

        recursos_insuficientes = ""
        if not possui_recurso(sobrevivente_1_obj, recursos_sobrevivente_1):
            recursos_insuficientes += "'sobrevivente_1': Não Possui Recursos Suficientes para a Troca. "
        if not possui_recurso(sobrevivente_2_obj, recursos_sobrevivente_2):
            recursos_insuficientes += "'sobrevivente_2': Não Possui Recursos Suficientes para a Troca. "
        if recursos_insuficientes != "":
            return Response(
                data = {"detalhes": recursos_insuficientes},
                status = status.HTTP_400_BAD_REQUEST
            )

        adicionar_recursos(sobrevivente_1_obj, recursos_sobrevivente_2)
        decrementar_recursos(sobrevivente_1_obj, recursos_sobrevivente_1)

        adicionar_recursos(sobrevivente_2_obj, recursos_sobrevivente_1)
        decrementar_recursos(sobrevivente_2_obj, recursos_sobrevivente_2)
        
        return Response(
            data={"detalhes": "Troca Realizada com Sucesso."},
            status=status.HTTP_200_OK
        )