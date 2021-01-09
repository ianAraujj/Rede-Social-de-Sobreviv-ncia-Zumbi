from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from sobreviventes.Views.Sobrevivente_view import SobreviventeViewSet
from sobreviventes.Views.RelatoContaminacao_view import RelatoContaminacaoViewSet
from sobreviventes.Views.Item_view import ItemViewSet
from sobreviventes.Views.Recursos_view import RecursoViewSet

urlpatterns = [

    path('cadastrar/', SobreviventeViewSet.as_view({
        'post': 'create'
    }), name='cadastrar-sobrevivente'),

    path('login/', obtain_jwt_token),

    path('sobrevivente/', SobreviventeViewSet.as_view({
        'get': 'list',
        'put': 'update'
    }), name='sobrevivente'),

    path('relatarInfectado/', RelatoContaminacaoViewSet.as_view({
        'post': 'create'
    }), name='relatar-contaminacao'),

    path('item/', ItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='itens'),

    path('recursos/trocar/', RecursoViewSet.as_view({
        'post': 'create'
    }), name='trocar-recursos')
]
