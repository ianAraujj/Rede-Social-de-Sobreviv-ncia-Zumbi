from django.urls import path
from relatorios.views import InfectadosViewSet, NaoInfectadosViewSet, RecursoPorSobrevivente, PontosPerdidos

urlpatterns = [

    path('infectados/', InfectadosViewSet.as_view({
        'get': 'list'
    }), name='sobreviventes-infectados'),

    path('NaoInfectados/', NaoInfectadosViewSet.as_view({
        'get': 'list'
    }), name='sobreviventes-nao-infectados'),

    path('recurso/sobrevivente/', RecursoPorSobrevivente.as_view({
        'get': 'list'
    }), name='recurso-por-sobrevivente'),

    path('pontosPerdidos/', PontosPerdidos.as_view({
        'get': 'list'
    }), name='pontos-perdidos')

]
