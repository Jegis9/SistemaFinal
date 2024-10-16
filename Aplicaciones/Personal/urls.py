from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
path('personal/<int:user_id>/', views.personal, name='personal'),
path('experiencia/', views.experiencia, name='experiencia'),
path('habilidades/', views.habilidades, name='habilidades'),
path('certificaciones/', views.certificaciones, name='certificaciones'),
path('educacion/', views.educacion, name='educacion'),
]

