from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from data.models import Products, Customer, Orders
from django.conf import settings
import razorpay

# Customer delivery address 
def deliver_add(request, id):

  product_det = Products.objects.get(product_id = id)  
  c_id = request.session.get('customer_id') 
  customer_details = Customer.objects.get(user_id = c_id)
  
  if product_det.product_stock == 0:
    messages.error(request, "Product Current Not Avalible")
    return redirect('product')
  
  if request.method == "POST":
    
    new_zipcode = request.POST.get('zipcode')
    
    if  new_zipcode :
      door = request.POST.get('door', "").strip()
      street = request.POST.get('st', "").strip()
      village = request.POST.get('vg', "").strip()
      mandal = request.POST.get('mdl', "").strip()
      district = request.POST.get('dist', "").strip()
      delv_add = (f"{door}, {street}, {village}, {mandal}, {district} - {new_zipcode}")
    else:
      delv_add = customer_details.address
      
    request.session["shipping_add"] = delv_add
    request.session["product_id"] = product_det.product_id
    
    return redirect('payment_page')
  
  content = {
    "product": product_det,
    "customer":  customer_details
  }
  return render(request, "product_buy.html", content)

# customer payment
def payment_page(request):
  
  id = request.session.get('product_id')
  address = request.session.get('shipping_add')
  
  try:
    product = Products.objects.get(product_id = id)
  except Products.DoesNotExist:
    messages.error(request, "Product details does Not Match")
    return redirect('product')
    
  c_id = request.session.get('customer_id')
  customer = Customer.objects.get(user_id = c_id)
  
  if request.method == "POST":
    qnty = int(request.POST.get('quantity'))
    payment_type = request.POST.get('payment_type')  
    
    if qnty > product.product_stock:
      messages.error(request, f"Product stock is not avalible: {product.product_stock}")
      return redirect('payment_page')
    
    total_amount = product.product_price * qnty
    
    order = Orders.objects.create(
      user = customer,
      vendor = product.vendor,
      product = product,
      quantity = qnty,
      shipping_address = address,
      order_amount = total_amount,
      order_status = "CREATED",
      payment_type = payment_type,
      payment_status = "PENDING"    
    )
    
    request.session['order_id'] = order.order_id
    request.session['quantity'] = qnty
     
    if payment_type == "CASH ON DELIVERY": 
      
      if product.product_stock >= qnty:
        product.product_stock -= qnty
        product.save()
      else:
        messages.error(request, "Insufficient stock")
        return redirect('product')
      
      order.order_status = "CONFIRMED"
      order.payment_status = "CASH ON DELIVERY"
      order.save()
      
      messages.success(request, "Order Placed Sucessfully ")
      return redirect('orders')
      
    client = razorpay.Client(
      auth = (settings.RAZORPAY_KEY_ID ,settings.RAZORPAY_KEY_SECRET)
    )
    
    razorpay_order = client.order.create({   #type: ignore
      "amount" : order.order_amount * 100,
      "currency" : "INR",
      "payment_capture" : 1
    })
    
    order.razorpay_order_id = razorpay_order['id']
    order.save() 
    
    return JsonResponse({
    "razorpay_key": settings.RAZORPAY_KEY_ID,
    "amount": order.order_amount * 100,
    "razorpay_order_id": order.razorpay_order_id
    })

    
  return render(request, "payment_page.html", {'product': product})
  
  
def resume_payment(request,id):
  try:
    order = Orders.objects.get( order_id = id, payment_type = "online", payment_status = "PENDING")
  except Orders.DoesNotExist:
    messages.error(request, "Invalid or Payment Already completed")
    return redirect('orders')

  client = razorpay.Client(
    auth= (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
  )
  
  if not order.razorpay_order_id:
    razorpay_order = client.order.create({ #type: ignore
      "amount": order.order_amount * 100,
      "currency": "INR",
      "payment_capture": 1
    })
    order.razorpay_order_id = razorpay_order['id']
    order.save()
    
  return render(request, "payment_page.html", {
      "product": order.product,
      "order": order,
      "razorpay_key": settings.RAZORPAY_KEY_ID,
      "amount": order.order_amount * 100,
      "auto_open": True
  })
  
  
def payment_success(request):
  payment_id = request.GET.get('payment_id')
  razorpay_id = request.GET.get('order_id')
  signature_id = request.GET.get('signature')
  
  order = Orders.objects.get(razorpay_order_id = razorpay_id)
  product = order.product
  # product = Products.objects.get(product_id = product_id)
  
  qnty = order.quantity
  
  client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
  )
  
  try:
    client.utility.verify_payment_signature({ #type: ignore
      'razorpay_order_id': razorpay_id,
      'razorpay_payment_id': payment_id,
      'razorpay_signature': signature_id
    })

    order.razorpay_payment_id = payment_id
    order.razorpay_signature = signature_id
    order.payment_status = "PAID"
    order.order_status = "CONFIRMED"
    order.save()
    
    if product.product_stock >= qnty:
      product.product_stock -= qnty
      product.save()
    
    messages.success(request, "Order Placed Successfully")
    return redirect('orders')
  
  except razorpay.error.SignatureVerificationError:  #type: ignore
      order.payment_status = "FAILED"
      order.save()
      messages.error(request, "Payment verification failed")
      return redirect('payment_page')
  
  
    
  
  
  


