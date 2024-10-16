from django.urls import path
from . import views

urlpatterns = [
    
    #  path('usuarios/', views.perfil, name='usuarios'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_cv, name='editar_cv'),

    path('agregar_experiencia/', views.agregar_experiencia, name='agregar_experiencia'),
    path('perfil/experiencia/editar/<int:experiencia_id>/', views.editar_experiencia, name='editar_experiencia'),
    path('perfil/experiencia/eliminar/<int:experiencia_id>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    
    path('perfil/certificado/agregar/', views.agregar_certificado, name='agregar_certificado'),
    path('perfil/certificado/editar/<int:certificado_id>/', views.editar_certificado, name='editar_certificado'),
    path('perfil/certificado/eliminar/<int:certificado_id>/', views.eliminar_certificado, name='eliminar_certificado'),
    
    # # path('perfil/generar-cv/', views.generar_cv, name='generar_cv'),
    path('perfil/generar-cv/', views.generar_cv_reportlab_individual, name='generar_cv_reportlab_individual'),
    path('generar_cv_pdf/<int:user_id>/', views.generar_cv_reportlab_platypus, name='generar_cv_reportlab'),


    path('prueba/', views.prueba, name='prueba'),
    path('prueba2/', views.prueba2, name='prueba2'),
    
    path('perfil_cv/<int:user_id>/', views.perfil_cv, name='perfil_cv'),
    
]
