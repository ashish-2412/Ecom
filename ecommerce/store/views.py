from django.shortcuts import render

# Create your views here.
def cart(request):
    return render(request,"store/cart.html")
def homepage(request):
    return render(request,"store/homepage.html")
def checkout(request):
    return render(request,"store/checkout.html")