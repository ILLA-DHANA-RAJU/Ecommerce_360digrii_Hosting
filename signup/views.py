from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.contrib.auth.models import User
from data.models import Customer, Vendor
from home.decorators import customer_login_required, vendor_login_reqired

# customer signup details code
def signup_view(request):
  if request.method == "POST":
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    altmobile =request.POST.get('altmobile')
    address = request.POST.get('address')
    zipcode = request.POST.get('zipcode')
    image = request.FILES.get('image')
    password = request.POST.get('password')
    
    if not firstname or not lastname or not email or not mobile or not address or not zipcode or not image:
      return render(request, "signup.html", {"error": "Please fill all requeired fields"})
    
    if Customer.objects.filter(email = email).exists():
      return render(request, "signup.html", {"error": "Email already existed try another email ✉"})
    
    if Vendor.objects.filter(email = email).exists():
      return render(request, "signup.html", {"error": "Email already exited in vendor data use another email ✉"})
    
    # if not firstname or not lastname or not email or not mobile or not address or not zipcode or not image:
    #   return messages.error(request, 'Please fill all requeired fields')
    
    # if Customer.objects.filter(email = email).exists():
    #   return messages.error(request, "Email already existed try another email ✉")
    
    # if Vendor.objects.filter(email = email).exists():
    #   return messages.error(request, "Email already exited in vendor data use another email ✉")
    
    hash_password = make_password(password)
  
    user_details = Customer(firstname=firstname, lastname=lastname, email=email,mobileno = mobile, alternate_mobileno = altmobile, address =address, zipcode = zipcode, image=image, user_password = hash_password )
    user_details.save()
    messages.success(request, "Successfully saved data")
    return redirect('login')
  return render(request, "signup.html", {'hidden_search': True})


@customer_login_required
def profile(request):
  user_ids = request.session['customer_id']
  user_details = Customer.objects.get(user_id = user_ids)
  return render(request, "profile.html", {"details": user_details})

# updating customer details code
@customer_login_required
def update_customer(request, id):
  
  c_val = request.session.get('customer_id') 
  if c_val != id:
    messages.error(request, "Access denied")
    return redirect('profile')
  
  customer = Customer.objects.get(user_id = c_val)
    
  try:
    if request.method == "POST":
      customer.firstname = request.POST.get('firstname')
      customer.lastname = request.POST.get('lastname')
      customer.email = request.POST.get('email')
      customer.mobileno = request.POST.get('mobile')
      customer.alternate_mobileno = request.POST.get('altmobile')
      customer.address = request.POST.get('address')
      customer.zipcode = request.POST.get('zipcode')
      if request.FILES.get('img'):
        customer.image = request.FILES.get('img')
      customer.save()
      messages.success(request, "Details update successfully")
      return redirect('profile')
    return render(request, 'customer_update.html', {"user": customer})
  except:
    messages.error(request, "Details Updating Iusse try to contect Team!")
    return render(request, 'customer_update.html')
  
# delete customer details code
@customer_login_required
def delete_customer(request, id):
  delete_user = Customer.objects.get(user_id = id)
  if delete_user:
    delete_user.delete()
    request.session.flush()
    messages.success(request, "Account Delete Successfully")
    return redirect("login")
  else:
    return render(request, "profile.html")
  
# Vendor signup details code
def vendor_signin(request):
  
  if request.method == "POST":
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    ven_type = request.POST.get('category')
    image = request.FILES.get('image')
    password = request.POST.get('password')
    
    if not firstname or not lastname or not email or not mobile or not ven_type or not password:
      return render(request, "vendor_signup.html", {"error": "Please fill all Required fields"})
    
    if Vendor.objects.filter(email = email).exists():
      return render(request, "vendor_signup.html", {"error": "Email already existed try another email ✉"})
    
    if Customer.objects.filter(email = email).exists():
      return render(request, "vendor_signup.html", {"error": "Email already exited in customer data use another email ✉"})
    
    hash_pass = make_password(password)
    
    ven_save = Vendor(firstname= firstname, lastname=lastname, email=email,mobileno = mobile, vendor_type = ven_type, image = image, vendor_password = hash_pass)
    messages.success(request, "Details Saved Successfully")
    ven_save.save()
    return redirect('vendor_login')
  return render(request, "vendor_signup.html", {'hidden_search': True})

@vendor_login_reqired
def vendor_profile(request):
  user_ids = request.session['vendor_id']
  vendor_ids = Vendor.objects.get(vendor_id = user_ids)
  return render(request, "vendor_profile.html", {"details": vendor_ids})

@vendor_login_reqired
def vendor_update(request, id): 
  v_val = request.session.get('vendor_id')
  
  if v_val != id:
    messages.error(request, "Access denied")
    return redirect('vendor_profile')
  
  vendor_up = Vendor.objects.get(vendor_id = v_val)
  
  try:
    if request.method == "POST":
      vendor_up.firstname = request.POST.get('firstname')
      vendor_up.lastname = request.POST.get('lastname')
      vendor_up.email = request.POST.get('email')
      vendor_up.mobileno = request.POST.get('mobile')
      
      if request.POST.get('category'):
        vendor_up.vendor_type = request.POST.get('category')
        
      request.session['ven_type'] = vendor_up.vendor_type
      
      if request.FILES.get('img'):
        vendor_up.image = request.FILES.get('img')
        
      vendor_up.save()
      messages.success(request, "Data Successfully updated")
      return redirect('vendor_profile')
  except Exception as e:
    messages.error(request, f"Error while updating time: {e}")
  
  return render(request, 'vendor_update.html', {"vd": vendor_up})


def vendor_delete(request, id):
  vd = Vendor.objects.get(vendor_id = id)
  if not vd:
    messages.error(request, "Details Not Found")
    return redirect('vendor_profile')
  else:
    vd.delete()
    messages.success(request, "Account Deleted Successfully")
    request.session.flush()
    return redirect('vendor_login')
    
    
    
      
      
  
    
  
  

















# Create your views here.
# @api_view(["POST"])
# def signup_views(request):
#   firstname = request.data.get('firstname')
#   lastname = request.data.get('lastname')
#   email = request.data.get('email')
#   mobile = request.data.get('mobile')
#   altmobile = request.data.get('altmobile')
#   address = request.data.get('address')
#   zipcode = request.data.get('zipcode')
#   image = request.FILES.get('image')
#   password = request.data.get('password')
  
#   if Customer.objects.filter(email=email).exists():
#     return Response({"error": "User details already exists"}, status=400)
  
#   user = Customer.objects.create(
#     firstname = firstname,
#     lastname=lastname,
#     email=email,
#     mobileno =mobile,
#     alternative_mobilno = altmobile,
#     address = address,
#     zipcode =zipcode,
#     image = image,
#     user_password = password
#   )  
#   return Response({"msg" : "Your details success full saved"})
