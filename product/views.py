from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class Index(ListView):
    model = Product
    template_name = 'product/index.html'
    paginate_by = 6
    context_object_name = 'products'


class Details(DetailView):
    model = Product
    template_name = 'product/detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'
