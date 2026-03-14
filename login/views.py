from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from home.decorators import customer_login_required
from data.models import Customer, Vendor
from django.contrib import messages

# Create your views here.
def login_view(request):
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    if Vendor.objects.filter(email=email):
      messages.error(request, "Email Already Existed in Vendor details")
      return redirect('login')
    
    try:
      user_details = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
      return render(request, "login.html", {"error": "Email Does Not Exist! Signup 👇🏻"})
    
    if check_password(password, user_details.user_password):
      request.session['customer_id'] = user_details.user_id
      request.session['customer_firstname'] = user_details.firstname
      request.session['customer_email'] = user_details.email
      return redirect('product') 
    else:
      messages.error(request, "Check Password")
      return redirect('login')
      
  return render(request, "login.html", {'hidden_search': True}) 

@customer_login_required
def user_logout(request):
  request.session.flush()
  return redirect('custome_login')


def vendor_login(request):
  if request.method == "POST":
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    if Customer.objects.filter(email=email):
      messages.error(request, "Email Already Existed in Customer details")
      return redirect('vendor_login')
    
    try:
      vendor_details = Vendor.objects.get(email=email)
    except Vendor.DoesNotExist:
      return render(request, "vendor_login.html", {"error": "Email Does Not Exist! Signup 👇🏻"})
    
    
    if check_password(password, vendor_details.vendor_password):
      request.session['vendor_id'] = vendor_details.vendor_id
      request.session['vendor_email'] = vendor_details.email
      request.session['vendor_firstname'] = vendor_details.firstname
      request.session['ven_type'] = vendor_details.vendor_type
      return redirect('dashboard')
    else:
      messages.error(request, "Check Password")
      return redirect('vendor_login')
    
  return render(request, "vendor_login.html", {'hidden_search': True})


def vendor_logout(request):
  request.session.flush()
  return redirect('custome_login') 