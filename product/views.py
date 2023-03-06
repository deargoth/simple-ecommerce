from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView, View


class Index(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 3


class Details(DetailView):
    model = Product
    template_name = 'product/details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
