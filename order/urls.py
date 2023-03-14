from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('saveorder/', views.SaveOrder.as_view(), name="save_order")
]
