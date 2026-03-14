from django.shortcuts import render,redirect
# from login.views import login_view
from home.decorators import customer_login_required
from django.contrib import messages
from data.models import Products

# This cart details.
def cart_data(req):
  if req.user.is_authenticated:
    return redirect('cart')
  else:
    messages.error(req, "Login and Happy Shopping 🛒")
    return redirect('login')

#This is dummy code for add cart in home page
def add_list(request):
  # item_details = request.GET.get('')
  count = request.session.get("count_incr", 0)
  count +=1
  request.session["count_incr"] = count
  return redirect('home')

#This is dummy code for Remove cart data in home page
def remove_list(request):
  remove = request.session.get('count_incr', 0)
  if remove > 0:
   remove -=1
   request.session['count_incr'] = remove
   return redirect('home')
  elif remove == 0:
    messages.error(request, "You must add an item to your cart before you can remove something.")
    return redirect('home')
  else: 
    return redirect('home')
  
  
# This is customer cart page
@customer_login_required
def cart_page(request):
  return render(request, "cartpage.html")

def add_cart(request, id):
  p_id = str(id)
  cart = request.session.get("cart", {})
  if  p_id  in cart:
    cart[p_id] +=  1
  else:
    cart[p_id] = 1
  request.session['cart'] = cart
  return redirect('cart_show')  


def show_cart(request):
  cart = request.session.get('cart', {})
  product_ids = [int(pid) for pid in cart.keys()]
  products = Products.objects.filter(product_id__in = product_ids)
  items = []
  total_amount = 0

  for p in products:
    qty = cart.get(str(p.product_id), 0)
    items.append({
      'product': p,
      'quantity': qty
    })  
    total_amount += p.product_price * qty
  return render(request, "cartpage.html", {"items": items, "total": total_amount})

def rm_cart(request, id):
  cart = request.session.get("cart", {})
  product = str(id)
  if product in cart:
    del cart[product]  
  request.session['cart'] = cart
  return redirect('cart_show')

def incr_pro(request, id):
  cart = request.session.get('cart', {})
  pro = str(id)
  if pro in cart:
    cart[pro] +=1  
  request.session['cart'] = cart
  return redirect('cart_show') 

def dcr_pro(request, id):
  cart = request.session.get('cart', {})
  pro = str(id)
  if pro in cart:
    cart[pro] -=1 
    try:
      if cart[pro] <= 0:
        del cart[pro]  
    except Exception as e:
      messages.error(request, f"Iusse is: {e}")
      return redirect('cart_show')
  request.session['cart'] = cart
  return redirect('cart_show')   
  