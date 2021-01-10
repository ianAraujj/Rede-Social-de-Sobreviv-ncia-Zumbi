# rest framework
from rest_framework import generics, status
from rest_framework.response import Response

# app: sobreviventes
from sobreviventes.models import Localidade, Itens, Sobrevivente, RelatoContaminacao, Recurso


def encontrar_localidade(latitude, longitude):

    try:
        localidade = Localidade.objects.get(latitude=latitude, longitude=longitude)
    except:
        localidade = None
    
    return localidade

def cadastrar_sobrevivente(dados_validados, usuario, localidade):

    novo_sobrevivente = Sobrevivente.objects.create(
        usuario=usuario,
        nome=dados_validados['nome'],
        idade=dados_validados['idade'],
        sexo=dados_validados['sexo'],
        ultimo_local=localidade,
    )
    
    return novo_sobrevivente

def encontrar_item(nome):

    try:
        item = Itens.objects.get(nome=nome)
    except:
        return None
    
    return item

def encontrar_recurso(item, sobrevivente):

    try:
        recurso = Recurso.objects.get(item=item,sobrevivente=sobrevivente)
    except:
        return None
    
    return recurso


def adicionar_recursos(sobrevivente, recursos):

    if recursos == None:
        return

    for i in recursos:

        try:
            item = encontrar_item(i['item'])
            quantidade = i['quantidade']

            recurso = encontrar_recurso(item, sobrevivente)

            if recurso == None:
                recurso = Recurso.objects.create(
                    item=item,
                    quantidade=quantidade,
                    sobrevivente=sobrevivente
                )
            else:
                recurso.quantidade = recurso.quantidade + quantidade
                recurso.save()
            
        except:
            pass


def decrementar_recursos(sobrevivente, recursos):

    if recursos == None:
        return

    for i in recursos:

        try:
            item = encontrar_item(i['item'])
            quantidade = i['quantidade']

            recurso = encontrar_recurso(item, sobrevivente)

            if recurso != None:
                recurso.quantidade = recurso.quantidade - quantidade
                recurso.save()
            
        except:
            pass


def localizar_sobrevivente(usuario):

    try:
        sobrevivente = Sobrevivente.objects.get(usuario=usuario)
        return sobrevivente
    except:
        return None


def verificar_limite_relatos(possivel_infectado):

    infectado = False

    numero_de_relatos = RelatoContaminacao.objects.filter(
        possivel_infectado = possivel_infectado
    ).count()

    if numero_de_relatos >= 3:
        infectado = True
    
    return infectado


def calcular_igualdade_troca(recursos_sobrevivente_1, recursos_sobrevivente_2):

    dados_invalidos = True
    igualdade = False

    if recursos_sobrevivente_1 == None or recursos_sobrevivente_2 == None:
        return dados_invalidos, igualdade
    
    try:

        pontos_lado_1 = calcular_pontos(recursos_sobrevivente_1)
        pontos_lado_2 = calcular_pontos(recursos_sobrevivente_2)

        if pontos_lado_1 == pontos_lado_2:
            igualdade = True
        dados_invalidos = False
        return dados_invalidos, igualdade

    except:
        return dados_invalidos, igualdade


def calcular_pontos(recursos):
    quantidade_pontos = 0

    for i in recursos:
        nome_item = i['item']
        quantidade_item = i['quantidade']
        item = encontrar_item(nome_item)

        quantidade_pontos = quantidade_pontos + (item.pontos * quantidade_item)
    
    return quantidade_pontos

def calcular_pontos_sobrevivente(sobrevivente):
    
    pontos = 0
    for recurso in Recurso.objects.filter(sobrevivente=sobrevivente):
        pontos += (recurso.quantidade * recurso.item.pontos) 
    
    return pontos


def possui_recurso(sobrevivente, possiveis_recursos):

    possui = False

    if possiveis_recursos == None:
        return possui
    
    for i in possiveis_recursos:

        item = encontrar_item(i['item'])
        quantidade = i['quantidade']

        recurso = encontrar_recurso(item, sobrevivente)
        if (recurso == None and quantidade > 0) or recurso.quantidade < quantidade:
            return possui

    possui = True    
    return possui