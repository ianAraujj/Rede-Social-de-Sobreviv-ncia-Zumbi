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

def encontrar_recurso(item, quantidade):

    try:
        recurso = Recurso.objects.get(item=item,quantidade=quantidade)
    except:
        return None
    
    return recurso


def adicionar_inventario(novo_sobrevivente, recursos):

    if recursos == None:
        return

    for i in recursos:

        try:
            item = encontrar_item(i['item'])
            quantidade = i['quantidade']

            recurso = encontrar_recurso(item, quantidade)

            if recurso == None:
                recurso = Recurso.objects.create(
                    item=item,
                    quantidade=quantidade
                )
            
            novo_sobrevivente.inventario.add(recurso)
            novo_sobrevivente.save()
            
        except:
            pass


def localizar_sobrevivente(usuario):

    try:
        sobrevivente = Sobrevivente.objects.get(usuario=usuario)
        return sobrevivente
    except:
        return None


