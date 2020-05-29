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
    receta = recetas.objects.get(id=id)
    ingredientes = ingredientesReceta.objects.filter(receta=id)
    pasos = pasosReceta.objects.filter(receta=id).order_by('pasoNumer')
    return render(request, 'mostrar.html', {'receta':receta,
                                            'ingredientes': ingredientes,
                                            'pasos':pasos})

def resExplorar(request):
    expReceta = recetas.objects.all()   
    return render(request, 'explorar.html',{'expReceta':expReceta})                                          

def resNosotros(request):
    return render(request, 'nosotros.html')

def resRegistro(request):
    return render(request, 'registro.html')

def crearReceta(request):
    if request.user.is_authenticated:
        return render(request, 'crearReceta.html')
    else:
        return redirect('login')

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

def misRecetas(request):
    receta = recetas.objects.filter(propietario=request.user.id)
    return render(request, 'misRecetas.html', {'recetas': receta})

def eliminarReceta(request, id):
    recetas.objects.filter(id=id).delete()
    return redirect('misRecetas')

def actualizarReceta(request, id):
    receta = recetas.objects.get(id=id, propietario=request.user.id)

    ingredientes = ingredientesReceta.objects.filter(receta=id)
    listaIngredientes = ""
    for element in ingredientes:
        listaIngredientes += element.ingredientes + ","
    cantIngredientes = ingredientes.count()

    pasos = pasosReceta.objects.filter(receta=id).order_by('pasoNumer')
    listaPasos = ""
    for element in pasos:
        listaPasos += element.paso + ","
    cantPasos = pasos.count()
    '''
    img = imgReceta.objects.filter(receta=id)
    listaImg = ""
    for element in pasos:
        listaImg += img.imagen + ","
    cantImg = img.count()'''
    return render(request, 'actualizarReceta.html', {'receta': receta,
                                                     'ingredientes': listaIngredientes,
                                                     'cantIngredientes': cantIngredientes,
                                                     'pasos': listaPasos,
                                                     'cantPasos': cantPasos,
                                                     #'img': listaImg,
                                                     #'cantImg': cantImg
                                                     })

def finActualizarReceta(request, id):
    if request.method == 'POST':
        #Actualiza datos generales de receta
        recetas.objects.filter(id=id).update(nombre=request.POST['nombre'],
                                descripcion=request.POST['descripcion'])
        recetaGeneral = recetas.objects.get(id=id)

        ######Actualizar pasos de receta
        #Borramos los pasos anteriores
        pasosReceta.objects.filter(receta=id).delete()
        #Iterador para guardar cada uno de los pasos nuevos
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

        ingredientesReceta.objects.filter(receta=id).delete()
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
    #Redirige a la página de crear receta
    return redirect('misRecetas')
