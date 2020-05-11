from django.urls import path
from . import views
urlpatterns = [
    path("cart/",views.cart,name="cart"),
    path("",views.homepage,name="homepage"),
    path("checkout/",views.checkout,name="checkout"),
    
]
