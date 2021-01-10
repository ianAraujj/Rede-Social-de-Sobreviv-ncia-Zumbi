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


class RelatarContaminacaoTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        inserir_dados_teste()


    def test_falha_token_nao_informado(self):

        url = reverse('relatar-contaminacao')
        resposta = self.client.post(url, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_falha_infectado_nao_informado(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        url = reverse('relatar-contaminacao')
        resposta = self.client.post(url, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data["detalhes"]["infectado_id"],
            "Este campo é obrigatório."
        )

    def test_falha_infectado_id_invalido(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        data = {
            "infectado_id": "iodndl"
        }

        url = reverse('relatar-contaminacao')
        resposta = self.client.post(url, data, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data["detalhes"]["infectado_id"],
            "Este campo deve ser Inteiro."
        )

    def test_falha_infectado_nao_encontrado(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        data = {
            "infectado_id": 3000
        }

        url = reverse('relatar-contaminacao')
        resposta = self.client.post(url, data, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            resposta.data["detalhes"]["infectado_id"],
            "Sobrevivente Informado Não foi Encontrado"
        )

    def test_sucesso(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        data = {
            "infectado_id": Sobrevivente.objects.all()[1].id
        }

        url = reverse('relatar-contaminacao')
        resposta = self.client.post(url, data, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            resposta.data["detalhes"],
            "Sinalização de Infectado Realizada com Sucesso."
        )

    def test_sucesso_relato_salvo(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        data = {
            "infectado_id": Sobrevivente.objects.all()[0].id
        }

        url = reverse('relatar-contaminacao')
        resposta = self.client.post(url, data, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            resposta.data["detalhes"],
            "Sinalização de Infectado Realizada com Sucesso."
        )
        self.assertEqual(
            RelatoContaminacao.objects.filter(
                relatado_por=sobrevivente,
                possivel_infectado=Sobrevivente.objects.all()[0]
            ).count(), 1
        )

    def test_falha_relato_ja_realizado(self):

        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        data = {
            "infectado_id": Sobrevivente.objects.all()[0].id
        }

        url = reverse('relatar-contaminacao')
        self.client.post(url, data, format='json')

        resposta_2 = self.client.post(url, data, format='json')

        self.assertEqual(resposta_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta_2.data["detalhes"],
            "Relato de Contaminação Já Realizado."
        )

    def test_segundo_relato(self):

        ## Relato 01
        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        data = {
            "infectado_id": Sobrevivente.objects.all()[0].id
        }

        url = reverse('relatar-contaminacao')
        self.client.post(url, data, format='json')

        ## Relato 02
        sobrevivente = Sobrevivente.objects.all()[1]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('relatar-contaminacao')
        self.client.post(url, data, format='json')

        ## 

        self.assertEqual(Sobrevivente.objects.all()[0].infectado, False)
        self.assertEqual(
            RelatoContaminacao.objects.filter(
                possivel_infectado=Sobrevivente.objects.all()[0]
            ).count(),
            2
        )

    def test_terceiro_relato_infectado(self):

        ## Relato 01
        sobrevivente = Sobrevivente.objects.all()[0]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))

        infectado_id = Sobrevivente.objects.all()[0].id
        data = {
            "infectado_id": infectado_id
        }

        url = reverse('relatar-contaminacao')
        self.client.post(url, data, format='json')

        ## Relato 02
        sobrevivente = Sobrevivente.objects.all()[1]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('relatar-contaminacao')
        self.client.post(url, data, format='json')

        ## Relato 03
        sobrevivente = Sobrevivente.objects.all()[2]
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(sobrevivente.usuario)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('relatar-contaminacao')
        self.client.post(url, data, format='json')

        ## 

        self.assertEqual(Sobrevivente.objects.get(
            id=infectado_id
        ).infectado, True)
        self.assertEqual(
            RelatoContaminacao.objects.filter(
                possivel_infectado=Sobrevivente.objects.get(id=infectado_id)
            ).count(),
            3
        )