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
from sobreviventes.utilitarios import calcular_pontos, calcular_pontos_sobrevivente


class CadastrarSobreviventeTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        inserir_dados_teste()


    def test_sucesso_cadastro_status_code(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "test",
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "78°",
                "longitude": "100°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def test_sucesso_cadastro(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "test",
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "78°",
                "longitude": "100°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        novo_sobrevivente = Sobrevivente.objects.latest('id')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(novo_sobrevivente.usuario.username, "test")
        self.assertEqual(novo_sobrevivente.nome, "test test")
        self.assertEqual(novo_sobrevivente.idade, 90)
        self.assertEqual(novo_sobrevivente.sexo, "Feminino")
        self.assertEqual(novo_sobrevivente.ultimo_local.latitude, "78°")

    def test_cadastro_verificar_recursos(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "test",
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "78°",
                "longitude": "100°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        novo_sobrevivente = Sobrevivente.objects.latest('id')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recurso.objects.filter(sobrevivente=novo_sobrevivente).count(), 2)
        self.assertEqual(Recurso.objects.get(
            sobrevivente=novo_sobrevivente,item=lista_itens[0]
        ).quantidade, 10)

    def test_falha_username_ja_existe(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "Maicon",
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "78°",
                "longitude": "100°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_falha_username_nao_informado(self):

        lista_itens = Itens.objects.all()

        dados = {
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "78°",
                "longitude": "100°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

        for mensagem_erro in resposta.data["detalhes"]["username"]:
            self.assertEqual(mensagem_erro, "Este campo não pode ser nulo.")

    def test_falha_nome_nao_informado(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "test",
            "password": "12345",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "78°",
                "longitude": "100°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        for mensagem_erro in resposta.data["detalhes"]["nome"]: 
            self.assertEqual(mensagem_erro, "Este campo não pode ser nulo.")

    def test_sucesso_localidade_salva(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "test",
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "300°",
                "longitude": "33°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')

        novo_sobrevivente = Sobrevivente.objects.latest('id')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            novo_sobrevivente.ultimo_local.longitude,
            "33°"
        )
        self.assertEqual(
            Localidade.objects.filter(latitude="300°", longitude="33°").count(),
            1
        )

    def test_sucesso_recursos_salvos(self):

        lista_itens = Itens.objects.all()

        dados = {
            "username": "test",
            "password": "12345",
            "nome": "test test",
            "idade": 90,
            "sexo": "Feminino",
            "ultimo_local": {
                "latitude": "300°",
                "longitude": "33°",
            },
            "recursos": [
                {
                    "item": lista_itens[0].nome,
                    "quantidade": 10
                },
                {
                    "item": lista_itens[3].nome,
                    "quantidade": 5,
                }
            ]
        }

        url = reverse('cadastrar-sobrevivente')
        resposta = self.client.post(url, dados, format='json')
        novo_sobrevivente = Sobrevivente.objects.latest('id')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            calcular_pontos(dados['recursos']),
            calcular_pontos_sobrevivente(novo_sobrevivente)
        )

        #print(calcular_pontos_sobrevivente(novo_sobrevivente))