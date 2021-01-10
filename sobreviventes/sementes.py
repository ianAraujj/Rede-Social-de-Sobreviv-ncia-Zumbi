from sobreviventes.models import Localidade, Itens, Sobrevivente, RelatoContaminacao, Recurso
from django.contrib.auth.models import User


def inserir_dados_teste():
    criar_localidades()
    criar_itens()
    criar_sobreviventes()
    inserir_recursos_sobrevivente()

def criar_localidades():

    Localidade.objects.create(
        latitude="78°",
        longitude="100°"
    )

    Localidade.objects.create(
        latitude="15°",
        longitude="180°"
    )

    Localidade.objects.create(
        latitude="230°",
        longitude="40°"
    )

def criar_itens():
    Itens.objects.create(
        nome="Agua",
        pontos=4
    )

    Itens.objects.create(
        nome="Alimentacao",
        pontos=3
    )

    Itens.objects.create(
        nome="Medicacao",
        pontos=2
    )

    Itens.objects.create(
        nome="Municao",
        pontos=1
    )

    Itens.objects.create(
        nome="Bateria",
        pontos=1
    )

def criar_sobreviventes():

    localidades = Localidade.objects.all()

    Sobrevivente.objects.create(
        usuario = User.objects.create(
            username="Maicon",
            password="12345"
        ),
        nome="Maicon",
        idade=20,
        sexo="Masculino",
        ultimo_local=localidades[0]
    )

    Sobrevivente.objects.create(
        usuario = User.objects.create(
            username="Cris",
            password="12345"
        ),
        nome="Cris",
        idade=14,
        sexo="Masculino",
        ultimo_local=localidades[1]
    )

    Sobrevivente.objects.create(
        usuario = User.objects.create(
            username="Tonia",
            password="12345"
        ),
        nome="Tonia",
        idade=7,
        sexo="Feminino",
        ultimo_local=localidades[2]
    )

    Sobrevivente.objects.create(
        usuario = User.objects.create(
            username="Julius",
            password="12345"
        ),
        nome="Julius",
        idade=40,
        sexo="Masculino",
        ultimo_local=localidades[0]
    )

    Sobrevivente.objects.create(
        usuario = User.objects.create(
            username="Greg",
            password="12345"
        ),
        nome="Greg",
        idade=11,
        sexo="Masculino",
        ultimo_local=localidades[1]
    )

    Sobrevivente.objects.create(
        usuario = User.objects.create(
            username="Rochelle",
            password="12345"
        ),
        nome="Rochelle",
        idade=37,
        sexo="Feminino",
        ultimo_local=localidades[2]
    )

def inserir_recursos_sobrevivente():

    itens = Itens.objects.all()
    sobrevivente = Sobrevivente.objects.all()

    ##

    Recurso.objects.create(
        item=itens[0],
        quantidade=10,
        sobrevivente=sobrevivente[0]
    )

    Recurso.objects.create(
        item=itens[0],
        quantidade=5,
        sobrevivente=sobrevivente[1]
    )

    Recurso.objects.create(
        item=itens[0],
        quantidade=1,
        sobrevivente=sobrevivente[3]
    )

    Recurso.objects.create(
        item=itens[0],
        quantidade=40,
        sobrevivente=sobrevivente[4]
    )

    Recurso.objects.create(
        item=itens[0],
        quantidade=0,
        sobrevivente=sobrevivente[5]
    )

    ##

    Recurso.objects.create(
        item=itens[1],
        quantidade=30,
        sobrevivente=sobrevivente[0]
    )

    Recurso.objects.create(
        item=itens[1],
        quantidade=100,
        sobrevivente=sobrevivente[1]
    )

    Recurso.objects.create(
        item=itens[1],
        quantidade=300,
        sobrevivente=sobrevivente[2]
    )

    Recurso.objects.create(
        item=itens[1],
        quantidade=4,
        sobrevivente=sobrevivente[3]
    )

    Recurso.objects.create(
        item=itens[1],
        quantidade=0,
        sobrevivente=sobrevivente[4]
    )

    Recurso.objects.create(
        item=itens[1],
        quantidade=7,
        sobrevivente=sobrevivente[5]
    )

    ##

    Recurso.objects.create(
        item=itens[2],
        quantidade=64,
        sobrevivente=sobrevivente[2]
    )

    Recurso.objects.create(
        item=itens[2],
        quantidade=32,
        sobrevivente=sobrevivente[4]
    )

    ##

    Recurso.objects.create(
        item=itens[3],
        quantidade=60,
        sobrevivente=sobrevivente[0]
    )

    Recurso.objects.create(
        item=itens[3],
        quantidade=30,
        sobrevivente=sobrevivente[1]
    )

    ##

    Recurso.objects.create(
        item=itens[4],
        quantidade=120,
        sobrevivente=sobrevivente[5]
    )