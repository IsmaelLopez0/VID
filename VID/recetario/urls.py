from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url, include
from django.contrib import admin
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('busqueda/', resBusqueda, name='resBusqueda'),
    path('nosotros/', resNosotros, name='resNosotros'),
    path('registro/', resRegistro, name='resRegistro'),
    path('crear_receta/', crearReceta, name='crearReceta'),
    path('regReceta/', guardarReceta, name='guardarReceta'),
    path('explorar/', resExplorar, name='resExplorar'),
    path('mostrar/<id>', mostrarReceta, name='mostrarReceta'),
]

urlpatterns += staticfiles_urlpatterns()
