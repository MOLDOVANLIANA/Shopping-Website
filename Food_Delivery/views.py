from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
import json
import datetime

from fooddelivery import settings
from .models import *
from django.db.models import Q
from .DBWrapper import DBWrapper

def home(request):
    return render(request, "Food_Delivery/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        mesaj=DBWrapper.Validate(username, email, fname, lname, pass1, pass2)
        if mesaj[0]==False:
             messages.error(request, mesaj[1])


        DBWrapper.ddddddddddddddddddddddddddddds 5 b (username, pass1, email, fname, lname)

        messages.success(request, "Your Account has been succesfully created! We have sent you a confirmation email!")

        # partea cu email-ul
        subject = "Welcome to Food Delivery!"
        message = "Hello " + fname + "!! \n" + "Welcome to FoodDelivery!! \nThank you for visiting our website\n."
        DBWrapper.SendMail(subject, message,email)

        return redirect('signin')

    return render(request, "Food_Delivery/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        success = DBWrapper.TryAuthenticate(request, username, pass1)
        if success[0]:
            return render(request, "Food_Delivery/main.html", {'fname': success[1]})

        else:
            messages.error(request, "Bad Credential")
            return redirect('home')

    return render(request, "Food_Delivery/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully")
    return redirect('home')

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems=order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems}
    return render(request, 'Food_Delivery/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems=order['get_cart_items']
    context = {'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, 'Food_Delivery/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'Food_Delivery/checkout.html', context)

def search(request):
    if request.method=='POST':
        searched=request.POST.get('searched')
        results= Product.objects.filter(name__contains=searched)

        return render(request, 'Food_Delivery/search.html', {'searched': searched, 'results':results})
    else:
        return render(request, 'Food_Delivery/search.html', {'searched': searched, 'results':results})

def updateItem(request):
        data=json.loads(request.body)
        productId=data['productId']
        action = data['action']

        print('Action:', action)
        print('productId:', productId)

        customer=request.user.customer
        product=Product.objects.get(id=productId)
        order, created=Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created=OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity=(orderItem.quantity+1)
        elif action == 'remove':
                orderItem.quantity=(orderItem.quantity-1)
        orderItem.save()

        if orderItem.quantity<=0:
            orderItem.delete()
        return JsonResponse('Item was added in the cart', safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id

        if total==order.get_cart_total:
            order.complete=True
        order.save()

        if order.shipping==True:
            ShipppingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('User is not loggin')
    return JsonResponse('Payment complete!', safe=False)