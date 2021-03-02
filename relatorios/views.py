# rest_framework

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import MethodNotAllowed
from pagseguro import PagSeguro

# app: sobreviventes
from sobreviventes.models import Sobrevivente, Recurso, Itens
from sobreviventes.serializers import SobreviventeSerializer


class InfectadosViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    queryset = Sobrevivente.objects.all()
    serializer_class = SobreviventeSerializer

    def list(self, request):

        quantidade_sobreviventes = Sobrevivente.objects.count()
        quantidade_infectados = Sobrevivente.objects.filter(infectado=True).count()
        porcentagem = round(float(quantidade_infectados / quantidade_sobreviventes) * 100, 2)
        porcentagem_string = str(porcentagem) + " %"

        retorno = {
            "Sobreviventes_Infectados": quantidade_infectados,
            "Porcentagem": porcentagem_string
        }

        return Response(
            data={"detalhes": retorno},
            status=status.HTTP_200_OK
        )

class NaoInfectadosViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    queryset = Sobrevivente.objects.all()
    serializer_class = SobreviventeSerializer

    def list(self, request):

        quantidade_sobreviventes = Sobrevivente.objects.count()
        quantidade_nao_infectados = Sobrevivente.objects.filter(infectado=False).count()
        porcentagem = round(float(quantidade_nao_infectados / quantidade_sobreviventes) * 100, 2)
        porcentagem_string = str(porcentagem) + " %"

        retorno = {
            "Sobreviventes_Nao_Infectados": quantidade_nao_infectados,
            "Porcentagem": porcentagem_string
        }

        return Response(
            data={"detalhes": retorno},
            status=status.HTTP_200_OK
        )

class RecursoPorSobrevivente(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    queryset = Sobrevivente.objects.all()
    serializer_class = SobreviventeSerializer

    def list(self, request):
        
        # Os Infectados Não São Contabilizados
        quantidade_sobreviventes = Sobrevivente.objects.filter(infectado=False).count()
        recursos_por_sobreviventes = []

        for item in Itens.objects.all():
            nome_item = item.nome
            quantidade_disponivel = 0

            recursos_item = Recurso.objects.filter(item=item)
            for recurso in recursos_item:
                # São Somados os recursos apenas dos Sobreviventes Nao Infectados
                if not recurso.sobrevivente.infectado:
                    quantidade_disponivel += recurso.quantidade
            
            media = round(float(quantidade_disponivel / quantidade_sobreviventes), 2)

            media_sobrevivente = {
                "Item": nome_item,
                "Quantidade": quantidade_disponivel,
                "Media_por_Sobrevivente": media
            }
            recursos_por_sobreviventes.append(media_sobrevivente)
        
        return Response(
            data={"detalhes": recursos_por_sobreviventes},
            status=status.HTTP_200_OK
        )

class PontosPerdidos(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    queryset = Sobrevivente.objects.all()
    serializer_class = SobreviventeSerializer

    def list(self, request):

        quant_pontos_perdidos_total = 0
        pontos_perdidos_list = []
        infectados = Sobrevivente.objects.filter(infectado=True)

        for infectado in infectados:
            pontos_perdidos_infectado = 0

            recursos_do_infectado = Recurso.objects.filter(sobrevivente=infectado)
            for recurso in recursos_do_infectado:
                pontos_perdidos_infectado += recurso.quantidade * recurso.item.pontos
            
            quant_pontos_perdidos_total += pontos_perdidos_infectado
            pontos_perdidos_list.append({
                "Infectado": infectado.nome,
                "Pontos_Perdidos": pontos_perdidos_infectado
            })
        
        resposta = {
            "Total_Pontos_Perdidos": quant_pontos_perdidos_total,
            "Detalhes": pontos_perdidos_list
        }
        return Response(
            data=resposta,
            status=status.HTTP_200_OK   
        )


class PagSeguroNotification(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    get_serializer_class = None

    def post(self, request, *args, **kwargs):
        notification_code = request.data['notificationCode']
        pg = PagSeguro(email="ianlucas2503@gmail.com", token="BC7D40CBF78449E1B355217F2B69EE67")
        notification_data = pg.check_notification(notification_code)
        print(notification_data)
        response = Response({"details": "ok"}, status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "https://sandbox.pagseguro.uol.com.br"
        return response