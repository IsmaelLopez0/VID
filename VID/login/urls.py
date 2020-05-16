from django.urls import path, include
from .views import *
#from django.views.generic.base import TemplateView

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name='login'),
    path('registrarse', newUser, name='newUser'),
    path('finRegistro', finRegistro, name='finRegistro'),
]
