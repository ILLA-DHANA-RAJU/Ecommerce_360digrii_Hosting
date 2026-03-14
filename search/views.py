from django.shortcuts import render
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from django.http import JsonResponse
from data.models import Products, Orders
from django.db.models import Q

# Search
# def search_details(request):
#   search_data = request.GET.get('q')
#   if search_data:   
#     result = Products.objects.filter(Q(product_name__icontains = search_data) | Q(product_type__icontains = search_data) | Q(product_description__icontains = search_data))
#     if result.exists():
#       return render(request, "home.html", {"fetch" : result}) 
#     else:
#       content ={
#         "message" : "Product details is Not Found With This Name: ",
#         "search_name" : search_data
#       }
#       return render(request, "home.html", content)
#   return render(request, "home.html")

def api_products(request):
  sd = request.GET.get('q', "")
  tepmlate = request.GET.get("template") or "home.html"
  
  if sd:
    search = Products.objects.filter( Q(product_name__icontains = sd) 
                                     |Q(product_specs__icontains = sd) 
                                     |Q(product_description__icontains = sd)
                                     |Q(product_type__icontains = sd))
  else: 
    search = Products.objects.none()
    
  fullhtml = render_to_string(tepmlate, {'fetch': search})
  
  suop = BeautifulSoup(fullhtml, "html.parser")
  
  card = suop.find("div", {"class":"card-group"})
  
  html =str(card) if card else "<p style='text-align: center;'>No Data Found</p>"
  return JsonResponse({'html' : html})

def api_orders(request):
  sd = request.GET.get('q', "")
  tepmlate = request.GET.get("template", "orders.html")
  
  if sd:
    search = Orders.objects.filter( Q(product__product_name__icontains = sd) )
  else: 
    search = Orders.objects.none()
    
  fullhtml = render_to_string(tepmlate, {'fetch': search})
  
  suop = BeautifulSoup(fullhtml, "html.parser")
  
  card = suop.find("div", {"class":"card-group"})
  
  html =str(card) if card else "<p>No Data Found</p>"
  return JsonResponse({'html' : html})