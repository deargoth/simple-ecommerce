from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, View


class Index(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 3
