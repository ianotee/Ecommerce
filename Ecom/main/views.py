from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .services import build_payment_request
import requests


import requests
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)



def Cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'Cart.html', context)




# Your other import statements and functions here
# @login_required(login_url='login')
# def payments(request):
    
#         # check if request is ajax or not
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             # get the payment method
#             order_number = request.POST.get('order_number')
#             transaction_id = request.POST.get('transaction_id')
#             payment_method = request.POST.get('payment_method')
#             status = request.POST.get('status')
#             print(order_number, transaction_id, payment_method, status)
            
#             order = Order.objects.get(order_number=order_number, user=request.user)
            
#             payment = Payment(
#                 user = request.user,
#                 transaction_id = transaction_id,
#                 payment_method = payment_method,
#                 amount = order.total,
#                 status = status   
#             )
#             payment.save()
            
#             order.payment = payment
#             order.is_ordered = True
#             order.save()
            
            
#             cart_items = Cart.objects.filter(user=request.user)
            
#             for item in cart_items:
#                 ordered_food = OrderedFood()
#                 ordered_food.order = order
#                 ordered_food.payment = payment
#                 ordered_food.user = request.user
                
#                 ordered_food.fooditem = item.fooditem
#                 ordered_food.quantity = item.quantity
#                 ordered_food.price = item.fooditem.price
#                 ordered_food.amount = item.fooditem.price * item.quantity
#                 ordered_food.save()
            
            
#             mail_subject = 'Thank you for ordering with us'
#             mail_template = 'orders/order_confirmation.html'
#             context = {
#                 'order': order,
#                 'user': request.user,
#                 'to_email': order.email,
#             }
#             send_notification(mail_subject, mail_template, context)
            
#             mail_subject = 'You have recieved a new order'
#             mail_template = 'orders/new_order.html'
#             to_emails = []
#             for i in cart_items:
#                 if i.fooditem.vendor.user.email not in to_emails:
#                     to_emails.append(i.fooditem.vendor.user.email)
                    
            
#             print(to_emails)
#             context = {
#                 'order': order,
#                 'user': request.user,
#                 'to_email': to_emails,
#             }
            
#             send_notification(mail_subject, mail_template, context)
            
#             cart_items.delete()
            
#             response ={
#                 'order_number': order.order_number,
#                 'transaction_id': transaction_id,
#             }
            
#             return JsonResponse(response)
        

#         return HttpResponse('payment successful')

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if request.method == 'POST':
        print('hello')
        build_payment_request()

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def details(request,pk):

	products =Product.objects.get(id=pk)

	context ={
		'products':products

	}

	return render(request, 'details.html',context)
