from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views  # Correct import

# rutas que serviran para poder manejar las rutas de esta aplicacion


urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('register/', views.register, name='register' ),
    path('registro_interno/', views.nuevo_registro, name='registro_interno' ),
    path('logout/', views.logout_view, name='logout_sale' ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('error', views.error, name='error'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_profile_externo/', views.edit_profile_externo, name='edit_profile_externo'),
    
]


