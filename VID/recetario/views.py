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
    if request.method == 'POST':
        #Guardar datos generales de receta
        recetaGeneral = recetas(nombre=request.POST['nombre'], ingredientes=request.POST['ingredientes'],
                                descripcion=request.POST['descripcion'], propietario=request.user,
                                imagenMuestra=request.FILES['imagenMuestra'])
        recetaGeneral.save()
        #Guardar imagenes extra de receta
        iterador = 1
        bandera = True
        while bandera:
            img = imgReceta(receta=recetaGeneral, imagen=request.FILES["image" + str(iterador)])
            img.save()
            iterador += 1
            try:
                print(request.FILES["image" + str(iterador)])
            except:
                bandera = False
        # Guardar pasos de receta
        iterador = 1
        bandera = True
        while bandera:
            paso = pasosReceta(receta=recetaGeneral, paso=request.POST["paso" + str(iterador)], pasoNumer=iterador)
            paso.save()
            iterador += 1
            try:
                print(request.POST["paso" + str(iterador)])
            except:
                bandera = False
        return redirect('index')
    return redirect('crearReceta')
