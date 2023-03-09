from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug>', views.Details.as_view(), name='details'),
    path('addtocart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('delfromcart/<int:pk>', views.DelFromCart.as_view(), name='del_from_cart'),
]
