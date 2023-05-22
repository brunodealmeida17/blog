from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models
from destaque.models import ImagesDestaque



class ListaNoticia(ListView):
    model = models.Noticia
    template_name = 'blog/lista.html'
    context_object_name = 'noticias'
    paginate_by = 30
    ordering = ['-id']

    def get_queryset(self):
        queryset = models.Noticia.available.all().order_by('id')
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["categories"] = models.Categoria.objects.all()
        context["municipios"] = models.Municipio.objects.all()
        context["files"] = ImagesDestaque.available.all()
        return context



