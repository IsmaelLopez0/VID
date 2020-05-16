from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.

def newUser(request):
    return render(request, 'registration/register.html')

def finRegistro(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = make_password(request.POST['password'])
    user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    user.save()
    return redirect('login')