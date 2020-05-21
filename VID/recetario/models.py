from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class recetas(models.Model):
    nombre = models.TextField()
    ingredientes = models.TextField()
    descripcion = models.TextField()
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    imagenMuestra = models.ImageField(upload_to ='imgRecetas/', blank=True, null=True)

class imgReceta(models.Model):
    receta = models.ForeignKey(recetas, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to ='imgRecetas/', blank=True, null=True)

class pasosReceta(models.Model):
    receta = models.ForeignKey(recetas, on_delete=models.CASCADE)
    paso = models.TextField()
    pasoNumer = models.SmallIntegerField()