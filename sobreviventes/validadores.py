# app: sobreviventes
from sobreviventes.models import Localidade, Itens, Sobrevivente, RelatoContaminacao, Recurso


def id_valido(id):
    try:
        int(id)
        return True
    except:
        return False


def validar_sobrevivente(sobrevivente_id):

    valido = False
    erro = ""
    codigo = 400

    if sobrevivente_id == None:
        erro = "Este campo é obrigatório."
        return valido, erro, codigo
    
    if not id_valido(sobrevivente_id):
        erro = "Este campo deve ser Inteiro."
        return valido, erro, codigo
    
    if Sobrevivente.objects.filter(id=sobrevivente_id).exists():
        valido = True
        codigo = 200
    else:
        erro = "Sobrevivente Informado Não foi Encontrado"
        codigo = 404
    
    return valido, erro, codigo