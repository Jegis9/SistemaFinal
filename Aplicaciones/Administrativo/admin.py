from django.contrib import admin
from .models import Insumos
from django.contrib.auth.models import Group



# cambia el titulo de la pagina de administracion
admin.site.site_header = 'Gestion de usuarios y grupos BMT'
# Register your models here.

# modelo para ser adminsitrado
admin.site.register(Insumos)



