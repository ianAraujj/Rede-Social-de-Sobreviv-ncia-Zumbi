from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from sobreviventes.Views.Sobrevivente_view import SobreviventeViewSet

urlpatterns = [
    path('cadastrar/', SobreviventeViewSet.as_view({
        'post': 'create'
    }), name='cadastrar-sobrevivente'),

    path('login/', obtain_jwt_token),

    path('sobrevivente/', SobreviventeViewSet.as_view({
        'put': 'update'
    }), name='sobrevivente')
]
