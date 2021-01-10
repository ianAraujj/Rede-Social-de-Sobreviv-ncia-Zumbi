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


class TrocarItensTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        inserir_dados_teste()


    def test_falha_requisicao_vazia(self):

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_falha_sobrevivente_2_nao_informado(self):

        dados = {}
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data["detalhes"]["sobrevivente_2"]["id"],
            "Este campo é obrigatório."
        )
    
    def test_falha_id_invalido(self):

        dados = {}
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        sobrevivente_2 = {
            "id": "kkkkkkkk",
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[1].nome,
                    "quantidade": 8
                }
            ]
        }

        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data["detalhes"]["sobrevivente_2"]["id"],
            "Este campo deve ser Inteiro."
        )

    def test_falha_sobrevivente_nao_encontrado(self):

        dados = {}
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        sobrevivente_2 = {
            "id": 10000,
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[1].nome,
                    "quantidade": 8
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            resposta.data["detalhes"]["sobrevivente_2"]["id"],
            "Sobrevivente Informado Não foi Encontrado"
        )

    def test_falha_sobreviventes_iguais(self):

        dados = {}
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[1].nome,
                    "quantidade": 8
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            resposta.data["detalhes"],
            "Os sobreviventes informados são iguais."
        )

    def test_falha_sobrevivente_infectado(self):

        dados = {}
        
        infectado = Sobrevivente.objects.all()[0]
        infectado.infectado = True
        infectado.save()
        sobrevivente_1 = {
            "id": infectado.id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[1].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[1].nome,
                    "quantidade": 8
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            resposta.data["detalhes"],
            "Os sobreviventes Infectados Não tem Permissão para Realizar Trocas."
        )

    def test_falha_itens_invalidos(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "nome": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "nome": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[1].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[1].nome,
                    "quantidade": 8
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data["detalhes"]["recursos"],
            "Este campo é obrigatório. Deve ser um array contendo os campos: 'item' (nome do item) e 'quantidade'."
        )


    def test_falha_desigualdade_troca(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 4
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[1].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 2
                },
                {
                    "item": Itens.objects.all()[1].nome,
                    "quantidade": 8
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data["detalhes"],
            "Não há uma Igualdade de Pontos para Realizar a Troca"
        )


    def test_falha_recursos_insuficientes(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 20
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 40
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[1].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 20
                },
                {
                    "item": Itens.objects.all()[4].nome,
                    "quantidade": 140
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data['detalhes'],
            "'sobrevivente_1': Não Possui Recursos Suficientes para a Troca. 'sobrevivente_2': Não Possui Recursos Suficientes para a Troca. "
        )

    def test_falha_recursos_insuficientes_sobrevivente_1(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 20
                },
                {
                    "item": Itens.objects.all()[2].nome,
                    "quantidade": 10
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[5].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[4].nome,
                    "quantidade": 100
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resposta.data['detalhes'],
            "'sobrevivente_1': Não Possui Recursos Suficientes para a Troca. "
        )


    def test_sucesso_ok(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 10
                },
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 30
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[5].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[4].nome,
                    "quantidade": 70
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_sucesso_recursos_decrementados(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 10
                },
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 30
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[5].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[4].nome,
                    "quantidade": 70
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Recurso.objects.get(
                sobrevivente=Sobrevivente.objects.all()[0],
                item=Itens.objects.all()[0]
            ).quantidade, 0
        )
        self.assertEqual(
            Recurso.objects.get(
                sobrevivente=Sobrevivente.objects.all()[0],
                item=Itens.objects.all()[3]
            ).quantidade, 30
        )
        self.assertEqual(
            Recurso.objects.get(
                sobrevivente=Sobrevivente.objects.all()[5],
                item=Itens.objects.all()[4]
            ).quantidade, 50
        )

    def test_sucesso_recursos_adicionados(self):

        dados = {}
        
        sobrevivente_1 = {
            "id": Sobrevivente.objects.all()[0].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[0].nome,
                    "quantidade": 10
                },
                {
                    "item": Itens.objects.all()[3].nome,
                    "quantidade": 30
                }
            ]
        }
        sobrevivente_2 = {
            "id": Sobrevivente.objects.all()[5].id,
            "recursos": [
                {
                    "item": Itens.objects.all()[4].nome,
                    "quantidade": 70
                }
            ]
        }
        dados["sobrevivente_1"] = sobrevivente_1
        dados["sobrevivente_2"] = sobrevivente_2

        url = reverse('trocar-recursos')
        resposta = self.client.post(url, dados, format='json') 

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Recurso.objects.get(
                sobrevivente=Sobrevivente.objects.all()[0],
                item=Itens.objects.all()[4]
            ).quantidade, 70
        )
        self.assertEqual(
            Recurso.objects.get(
                sobrevivente=Sobrevivente.objects.all()[5],
                item=Itens.objects.all()[0]
            ).quantidade, 10
        )
        self.assertEqual(
            Recurso.objects.get(
                sobrevivente=Sobrevivente.objects.all()[5],
                item=Itens.objects.all()[3]
            ).quantidade, 30
        )