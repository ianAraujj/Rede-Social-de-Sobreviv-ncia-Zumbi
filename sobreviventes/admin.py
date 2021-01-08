from django.contrib import admin
from sobreviventes.models import Localidade, Itens, Sobrevivente, RelatoContaminacao, Recurso

admin.site.register(Localidade)
admin.site.register(Itens)
admin.site.register(Sobrevivente)
admin.site.register(RelatoContaminacao)
admin.site.register(Recurso)