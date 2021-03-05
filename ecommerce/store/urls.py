from django.urls import path
from . import views
app_name="store"
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("update_item/",views.updateitem,name="update_item"),
    path("process_order/",views.processOrder,name="process_order"),
    path("registration/",views.registration,name="registration"),
    path("login/",views.customer_login,name='customer_login'),
    path("logout/",views.customer_logout,name='customer_logout'),
    path("myorders/",views.customer_orders,name='customer_orders'),
    path("download_invoice/<int:pk>",views.downloadInvoice,name='download_invoice'),
    path("view_book/<int:pk>",views.viewBook,name='view_book')
]
