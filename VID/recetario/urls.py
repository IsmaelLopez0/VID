from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('busqueda/', resBusqueda, name='resBusqueda'),
]
