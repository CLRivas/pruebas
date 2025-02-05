from django.db import models

from django.db import models
from django.core.files import File
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone


# Create your models here.
class UtilsData(models.Model):
    """
    UtilsData es una clase abstracta que es llamada
    por otro modelo. este modelo se encargara
    de proveer a las tablas la
    fecha de creacion y la fecha de modificacion
    """
    user_created = models.ForeignKey(User,verbose_name="Usuario",on_delete=models.SET_NULL,null=True,blank=True)
    created = models.DateTimeField('creada el',auto_now_add=True,blank=True,null=True,help_text='La fecha de creacion de este objeto',)
    modified = models.DateTimeField('modificada el',auto_now=True,help_text='la fecha de modificacion de este objeto',)
    enable = models.BooleanField("Visible/No Visible", default=True)

    class Meta:
        # meta opciones
        abstract = True
        get_latest_by = "created"
        ordering = ['-created', '-modified']
        

class Usuario(UtilsData):
    nombre = models.CharField("Nombres",max_length=100)
    apellido = models.CharField("Apellidos",max_length=100)
    celular = models.CharField("Numero de Celular",max_length=15,null=True,blank=True)
    email = models.CharField("Email",max_length=100,null=True,blank=True)
    habilitado = models.BooleanField("Habilitado", default=True)
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.email = self.email.upper()
        super().save(*args, **kwargs)