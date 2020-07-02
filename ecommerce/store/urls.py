from django.urls import path
from . import views
urlpatterns = [
    path("cart/",views.cart,name="cart"),
    path("",views.homepage,name="homepage"),
    path("checkout/",views.checkout,name="checkout"),
    path("update_item/",views.updateitem,name="update_item"),
    path("process_order/",views.processOrder,name="process_order"),
    path("paytm_process/",views.paytm_process,name="paytm_process"),
    
]
