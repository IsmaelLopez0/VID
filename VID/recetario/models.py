from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class recetas(models.Model):
    nombre = models.TextField()
    ingredientes = models.TextField()
    descripcion = models.TextField()
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    imagen = models.ImageField(upload_to ='imgRecetas/', blank=True, null=True)