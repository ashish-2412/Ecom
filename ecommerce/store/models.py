from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=200,)
    email=models.EmailField(max_length=200,)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.IntegerField()
    digital=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    image=models.ImageField(null=True,blank=True)

    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url='/images/placeholder.png'
        return url

    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        items=self.orderitem_set.all()
        total=0
        for i in items:
            total+=i.get_total
        return total
    @property
    def get_cart_quantity(self):
        items=self.orderitem_set.all()
        total=0
        for i in items:
            total+=i.quantity
        return total
    @property
    def shipping(self):
        shipping=False
        orderItems=self.orderitem_set.all()
        for i in orderItems:
            if not i.product.digital:
                shipping=True
        return shipping

class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total
    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    pincode=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address