from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.

def newUser(request):
    '''
    Redirecciona a la página de registro de usuario.

    :param request: Contiene la información de la solicitud hecha por el navegador al igual que información del usuario.
    :return: pantalla de registro de usuario.
    '''
    return render(request, 'registration/register.html')

def finRegistro(request):
    '''
    Sirve para completar el proceso de registro de un usuario.

    :param request: Contiene la información de la solicitud hecha por el navegador al igual que información del usuario.
    :return:
        -render: te regresa a la pantalla de re registro de usuario con un código de error.
        -redirect: después de registrar el usuario te redirecciona a la pantalla de login para iniciar sesión.
    '''
    #Si la solicitud se hizo con el método POST
    if request.method == 'POST':
        #Sí el nombre de usuario ya se encuentra en la base de datos
        if User.objects.filter(username=request.POST['username']).exists():
            #Regresa a la pantalla de re registro de usuario con un código de error
            return render(request, 'registration/register.html', {'error': 1})
        #Sí el correo ya se encuentra registrado
        if User.objects.filter(email=request.POST['email']).exists():
            # Regresa a la pantalla de re registro de usuario con un código de error
            return render(request, 'registration/register.html', {'error': 2})
        #Guardamos en variables lo que se contiene en la solicitud mandada por el navegador
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        #Con make_password se convierte lo incluido en la cadena a una contraseña encriptada con pbkdf2
        password = make_password(request.POST['password'])
        #Creamos una variable modelo de usuario con las variables obtenidas anteriormente.
        user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        #Guardamos el modelo de usuario en la base de datos
        user.save()
        '''Por si se quiere iniciar sesión de forma inmediata en cuanto se registre
        
        from django.contrib.auth import authenticate #Esto estaria en la parte superior del documento
        #Variable para crear una solicitud de inicio de sesión
        iniciarSesion = authenticate(username=username, password=request.POST['password'])
        #Si iniciarSesión es diferente a nulo
        if iniciarSesion is not None:
            # Se inició sesión
            # Se recomienda redireccionar a index
        else:
            # No se inició sesión
            # Probablemente hubo un error desconocido por mi parte (Ismael)
        '''
    #Después de registrar el usuario te redirecciona a la pantalla de login para iniciar sesión
    return redirect('login')

def perfil(request):
    '''
    Muestra tu información de perfil y al modificar un valor te da la opción de actualizar tu información de perfil.
    Con este mismo método se actualizan los datos.

    :param request: Contiene la información de la solicitud hecha por el navegador al igual que información del usuario.
    :return:
        - render: Muestra la pantalla de perfil de usuario y de tener algún error se muestra.
        - redirect: Si el usuario no ha iniciado sesión te redirige a la pantalla de login
    '''
    #Si hay un usuario con sesión iniciada
    if request.user.is_authenticated:
        #Inicializamos la variable de la lista de errores y la que contendrá los datos de usuario
        errores = []
        user = None
        #Si la solicitud se hizo con el método POST
        if request.method == 'POST':
            #Obtenemos los datos del usuario que hizo la solicitud
            user = User.objects.get(id=request.user.id)
            #Si el nombre de usuario es diferente al nombre de usuario que tiene ya registrado
            if request.POST['username'] != request.user.username:
                #Si el nombre de usuario ya existe
                if User.objects.filter(username=request.POST['username']).exists():
                    #Guarda en la lista el error de nombre de usuario ya registrado
                    errores.append('El nombre de usuario ya se encuentra registrado.')
                    return render(request, 'perfil.html', {'error': errores, 'user': user})
            #Actualiza el usuario con los nuevos campos guardados
            User.objects.filter(username=request.POST['username'])\
                .update(first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'])
            #Obtenemos los datos actualizados del usuario
            print('3')
            user = User.objects.get(id=request.user.id)
        #Muestra la pantalla de perfil de usuario
        return render(request, 'perfil.html', {'user': user})
    #Si no hay un usuario con sesión iniciada
    else:
        #Redirecciona a la pantalla de login para que pueda
        return redirect('login')
