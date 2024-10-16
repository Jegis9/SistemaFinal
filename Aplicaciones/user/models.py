from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pdi = models.IntegerField(null=True, blank=True)  
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100, blank=True, null=True)
    lastname1 = models.CharField(max_length=100)
    lastname2 = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)  
    phone = models.CharField(max_length=15, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M')
    is_internal = models.BooleanField(default=False)
    image = models.ImageField(default='images_1.jpg', upload_to='Profile_images')


# cuando el usuario es creado en esta parte se asegura que el perfil es creado con su respectivo perfil
@receiver(post_save, sender=User) # primero se crea el perfil segun el usuario 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User) # y aqui se guarda el perfil que se creo segun el usuario relacion
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


