from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('<slug>', views.Details.as_view(), name="details"),
    # path('addtocart/', views.AddToCart.as_view(), name="addtocart"),
    # path('removefromcart/', views.RemoveFromCart.as_view(), name="removefromcart"),
    # path('cart/', views.Cart.as_view(), name="cart"),
    # path('finalize/', views.Finalize.as_view(), name="finalize"),
]
