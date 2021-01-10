from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

## app: sobreviventes
from sobreviventes.models import *
from sobreviventes.sementes import inserir_dados_teste


class AtualizarLocalizacaoTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        inserir_dados_teste()


    def test_falha_problemas_no_token(self):

        dados = {
            "latitude": "78°",
            "longitude": "100°",
        }

        url = reverse('sobrevivente')
        resposta = self.client.put(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_falha_latitude_nao_infomada(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        dados = {
            "longitude": "100°",
        }

        url = reverse('sobrevivente')
        resposta = self.client.put(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        for mensagem_erro in resposta.data["detalhes"]["latitude"]:
            self.assertEqual(
                mensagem_erro, 
                "Este campo é obrigatório."
            )

    def test_sucesso_status_code(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        dados = {
            "latitude": "78°",
            "longitude": "2°",
        }

        url = reverse('sobrevivente')
        resposta = self.client.put(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_sucesso_localidade_alterada(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        dados = {
            "latitude": "78°",
            "longitude": "2°",
        }

        url = reverse('sobrevivente')
        resposta = self.client.put(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Sobrevivente.objects.get(id=sobrevivente.id).ultimo_local.latitude,
            "78°"
        )
        self.assertEqual(
            Sobrevivente.objects.get(id=sobrevivente.id).ultimo_local.longitude,
            "2°"
        )