from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def resBusqueda(request):
    nombre = request.POST['buscar']
    busqueda = recetas.objects.filter(nombre=nombre)
    return render(request, 'busqueda.html', {'resultado': busqueda})

def resNosotros(request):
    return render(request, 'nosotros.html')

def resRegistro(request):
    return render(request, 'registro.html')

def crearReceta(request):
    return render(request, 'crearReceta.html')

def guardarReceta(request):
    nombre = request.POST['nombre']
    ingredientes = request.POST['ingredientes']
    descripcion = request.POST['descripcion']
    #descripcion = request.FILE['descripcion']
    propietario = request.user
    nuevaReceta = recetas(nombre=nombre, ingredientes=ingredientes, descripcion=descripcion,
                          propietario=propietario)
    nuevaReceta.save()
    return redirect('index')

