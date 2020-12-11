from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt
import requests
import razorpay
# Create your views here.
def homepage(request):
    cart_data=cartData(request)
    cartItems=cart_data['cartItems']
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/homepage.html',context)
def cart(request):
    cart_data=cartData(request)
    items=cart_data['items']
    order=cart_data['order']
    cartItems=cart_data['cartItems']
    return render(request,"store/cart.html",{"items":items,"order":order,"cartItems":cartItems})
def checkout(request):
    cart_data=cartData(request)
    items=cart_data['items']
    order=cart_data['order']
    cartItems=cart_data['cartItems']
    return render(request,"store/checkout.html",{"items":items,"order":order,"cartItems":cartItems})

def updateitem(request):
    data=json.loads(request.body)
    productID=data['productID']
    action=data['action']
    print(productID,action)
    customer=request.user.customer
    product=Product.objects.get(id=productID)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=="add":
        orderItem.quantity+=1
    elif action=="remove":
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
    else:
        customer,order=guestOrder(request,data )
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    if total==float(order.get_cart_total):
        order.complete=True
    order.save() 
    if order.shipping==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],    
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            pincode=data['shipping']['zipcode']

        )
    return JsonResponse('Payment Complete',safe=False)
    

