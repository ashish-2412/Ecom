from django.shortcuts import render,get_object_or_404
from .models import *
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect,FileResponse
import json
import datetime
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm,CustomerForm
from .utils import *
from .invoice import generateInvoice
from django.views.decorators.csrf import csrf_exempt
import requests
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
    
def registration(request):
    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        customer_form=CustomerForm(data=request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            customer=customer_form.save(commit=False)
            customer.user=user
            customer.save()
            registered=True
        else:
            print(user_form.errors,customer_form.errors)

    else:
        user_form=UserForm()
        customer_form=CustomerForm()
    return render(request,'store/registration.html',context={'registered':registered,'user_form':user_form,'customer_form':customer_form})

def customer_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('store:homepage'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Login failed")
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'store/login.html')
@login_required
def customer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:homepage'))
def customer_orders(request):
    cart_data=cartData(request)
    cartItems=cart_data['cartItems']
    orders=Order.objects.filter(customer=Customer.objects.filter(user=request.user)[0])
    order_items=[]
    for o in orders:
        order_items_i=list(OrderItem.objects.filter(order=o))
        print(order_items_i)
        order_items.extend(order_items_i)
    order_items.reverse()
    return render(request,'store/my_orders.html',{"orders":order_items,'cartItems':cartItems})

def downloadInvoice(request,pk):
    order_item=get_object_or_404(OrderItem,id=pk)
    path="invoices/invoices_"+str(order_item.pk)+".pdf"
    obj = generateInvoice(order_item.order.customer.user.username,order_item,order_item.pk)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def viewBook(request,pk):
    try:
        return FileResponse(open('static/digitalpdfs/samplebook.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()