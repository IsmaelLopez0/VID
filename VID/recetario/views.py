from django.shortcuts import render

# Create your views here.

def resBusqueda(request):
    saludo = "hola"
    return render(request, 'busqueda.html', {'saludo':saludo})

def resNosotros(request):
    return render(request, 'nosotros.html')

def resRegistro(request):
    return render(request, 'registro.html')
