from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def resBusqueda(request):
    buscar = request.POST['buscar']
    #Consulta like SQL... es nombreDelCampo__contains=valorABuscar
    resultado = recetas.objects.filter(nombre__contains=buscar)
    return render(request, 'busqueda.html', {'resultado': resultado,
                                             'buscar': buscar})                                          


def mostrarReceta(request, id):
    
    return render(request, 'mostrar.html', {'resultadoReceta': resultadoReceta})   

def resExplorar(request):
    expReceta = recetas.objects.all()   
    return render(request, 'explorar.html',{'expReceta':expReceta})                                          

def resNosotros(request):
    return render(request, 'nosotros.html')

def resRegistro(request):
    return render(request, 'registro.html')

def crearReceta(request):
    return render(request, 'crearReceta.html')

def guardarReceta(request):
    if request.method == 'POST':
        #Guardar datos generales de receta
        recetaGeneral = recetas(nombre=request.POST['nombre'],
                                descripcion=request.POST['descripcion'], propietario=request.user,
                                imagenMuestra=request.FILES['imagenMuestra'])
        recetaGeneral.save()
        ######Guardar imagenes extra de receta
        #Iterador para guardar cada una de las imagenes
        iterador = 1
        #Esta "bandera" se utiliza para que en cuanto ya no encuentre un siguiente elemento deje de intentar guardar
        bandera = True
        #Cilo para guardar las imagenes
        while bandera:
            #Guarda imagen
            try:
                img = imgReceta(receta=recetaGeneral, imagen=request.FILES["image" + str(iterador)])
                img.save()
                #Incrementa el iterador para obtener la siguiente imagen
                iterador += 1
            #Si falla el intento de guardar, la "bandera" cambia a false para que el ciclo se detenga
            except:
                bandera = False
        ######Guardar pasos de receta
        #Iterador para guardar cada una de los pasos
        iterador = 1
        #Esta "bandera" se utiliza para que en cuanto ya no encuentre un siguiente elemento deje de intentar guardar
        bandera = True
        #Cilo para guardar los pasos
        while bandera:
            #Guarda el paso de la receta
            paso = pasosReceta(receta=recetaGeneral, paso=request.POST["paso" + str(iterador)], pasoNumer=iterador)
            paso.save()
            # Incrementa el iterador para obtener el siguiente paso
            iterador += 1
            # Se intenta mostrar el contenido del siguiente paso a guardar
            try:
                print(request.POST["paso" + str(iterador)])
            except:
                # Si falla el intento la "bandera" cambia a false para que el ciclo se detenga
                bandera = False
        ######Guardar recetario de receta
        #Iterador para guardar cada una de los ingredientes
        iterador = 1
        #Esta "bandera" se utiliza para que en cuanto ya no encuentre un siguiente elemento deje de intentar guardar
        bandera = True
        #Cilo para guardar los ingredientes
        while bandera:
            #Guarda el paso de la receta
            ingrediente = ingredientesReceta(receta=recetaGeneral, ingredientes=request.POST["ingrediente" + str(iterador)])
            ingrediente.save()
            # Incrementa el iterador para obtener el siguiente paso
            iterador += 1
            # Se intenta mostrar el contenido del siguiente paso a guardar
            try:
                print(request.POST["ingrediente" + str(iterador)])
            except:
                # Si falla el intento la "bandera" cambia a false para que el ciclo se detenga
                bandera = False
        #Redirige a la pantalla principal
        return redirect('index')
    #Redirige a la página de crear receta
    return redirect('crearReceta')
