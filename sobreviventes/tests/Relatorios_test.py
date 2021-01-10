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


class RelatorioTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        inserir_dados_teste()


    def test_porcentagem_infectados(self):

        url = reverse('sobreviventes-infectados')
        resposta = self.client.get(url, format='json')
        
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data["detalhes"]['Sobreviventes_Infectados'],
            0
        )
        self.assertEqual(
            resposta.data["detalhes"]['Porcentagem'],
            "0.0 %"
        )

    def test_sucesso_porcentagem_infectados(self):

        infectado_1 = Sobrevivente.objects.all()[2]
        infectado_1.infectado = True
        infectado_1.save()

        infectado_2 = Sobrevivente.objects.all()[4]
        infectado_2.infectado = True
        infectado_2.save()


        url = reverse('sobreviventes-infectados')
        resposta = self.client.get(url, format='json')
        
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data["detalhes"]['Sobreviventes_Infectados'],
            2
        )
        self.assertEqual(
            resposta.data["detalhes"]['Porcentagem'],
            "33.33 %"
        )
    

    def test_porcentagem_nao_infectados(self):

        infectado_1 = Sobrevivente.objects.all()[2]
        infectado_1.infectado = True
        infectado_1.save()

        infectado_2 = Sobrevivente.objects.all()[4]
        infectado_2.infectado = True
        infectado_2.save()

        url = reverse('sobreviventes-nao-infectados')
        resposta = self.client.get(url, format='json')
        
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data["detalhes"]['Sobreviventes_Nao_Infectados'],
            4
        )
        self.assertEqual(
            resposta.data["detalhes"]['Porcentagem'],
            "66.67 %"
        )

    def test_recurso_por_sobrevivente(self):

        infectado_1 = Sobrevivente.objects.all()[1]
        infectado_1.infectado = True
        infectado_1.save()

        url = reverse('recurso-por-sobrevivente')
        resposta = self.client.get(url, format='json')
        
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data["detalhes"][0]['Quantidade'],
            51
        )
        self.assertEqual(
            resposta.data["detalhes"][0]['Media_por_Sobrevivente'],
            10.2
        )

    def test_pontos_perdidos_infectados(self):

        infectado_1 = Sobrevivente.objects.all()[1]
        infectado_1.infectado = True
        infectado_1.save()

        infectado_2 = Sobrevivente.objects.all()[3]
        infectado_2.infectado = True
        infectado_2.save()

        url = reverse('pontos-perdidos')
        resposta = self.client.get(url, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data['Total_Pontos_Perdidos'],
            366
        )

    def test_pontos_perdidos(self):

        infectado_1 = Sobrevivente.objects.all()[2]
        infectado_1.infectado = True
        infectado_1.save()

        url = reverse('pontos-perdidos')
        resposta = self.client.get(url, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data['Total_Pontos_Perdidos'],
            1028
        )