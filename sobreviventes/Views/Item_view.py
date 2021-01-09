# rest_framework

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import MethodNotAllowed

# app: sobreviventes
from sobreviventes.models import Itens
from sobreviventes.serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']
    queryset = Itens.objects.all()
    serializer_class = ItemSerializer
