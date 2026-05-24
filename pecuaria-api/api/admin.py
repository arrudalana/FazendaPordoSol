from django.contrib import admin
from .models import Dono, Animal, Leilao, Categoria

# Isso faz com que suas tabelas apareçam no painel administrativo
admin.site.register(Dono)
admin.site.register(Animal)
admin.site.register(Leilao)
admin.site.register(Categoria)