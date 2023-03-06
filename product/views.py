from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, View


class Index(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/index.html')
