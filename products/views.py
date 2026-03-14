from django.shortcuts import render, redirect
from data.models import Products,  Vendor, Feedback
from home.decorators import customer_login_required, vendor_login_reqired
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required

# Create your views here.
@customer_login_required
def products_data(request):
    fetch_data = Products.objects.all() 
    content = {
      "fetch" : fetch_data,
      "template_name": "product.html"
    }
    return render(request, "product.html", content)
  
# Single page product details page
def product_details(request, id, category):
  product = Products.objects.get(product_id = id)
  related_products = Products.objects.filter(product_type = category).exclude(product_id = id)
  feedback_data = Feedback.objects.filter(product_id = id)
  
  context = {
    "product": product,
    "fetch": related_products,
    "res" : feedback_data,
  }
  return render(request, "product_page.html", context)

@vendor_login_reqired
def product_manage(req):
  # ven = request.session.get('vendor_id')
  # p_data = Products.objects.filter(vendor_id = ven)
  return render(req, 'product_manage.html')

def api_manage(request):
  ven = request.session.get('vendor_id')
  
  draw = int(request.GET.get('draw', 1))
  start = int(request.GET.get('start', 0))
  length = int(request.GET.get('length', 10))
  search_data = request.GET.get("search[value]", "")
  order_columns = int(request.GET.get('order[0][column]', 0))
  order_dir = request.GET.get('order[0][dir]', 'desc')
  
  columns = ['product_name', 'product_type', 'product_price', 'product_stock', 'product_status', 'product_image', 'product_video']
  
  order_field = columns[order_columns]
  if order_dir == 'desc':
    order_field = '-' + order_field
  
  qr = Products.objects.filter(vendor_id = ven)
  if search_data:
    qr = qr.filter(Q(product_name__icontains = search_data) 
                 | Q(product_type__icontains = search_data) 
                 | Q(product_description__icontains = search_data)) 
     
  total_count = Products.objects.filter(vendor_id = ven).count()
  field_count = qr.count()
  
  qr = qr.order_by(order_field)[start:start+length]
  
  p_data =[]
  si = 1
  
  for q in qr:
    p_data.append({
      'si' : si,
      'name' : q.product_name,
      'type' : q.product_type,
      'price': q.product_price,
      'stock': q.product_stock,
      'image': f"<img src='/media/{q.product_image}' alt='image loading...' width='70px' />" 
                if q.product_image else "No image Found",
      'video' : (
        f'<video width="200px" height="120px" controls><source src="/media/{q.product_video}" type="video/mp4"></video>'
      )
      if q.product_video else "No Video Found",
      'operations' : (
        f"<a href='/update/products/{q.product_id}/' class='update'>Update</a>"
        f' | '
        f'<a href="/delete/products/{q.product_id}/" class="delete">Delete</a>'
      )  
    })
    si+=1

  return JsonResponse({
    'draw': draw,
    'recordsTotal': total_count,
    'recordsFiltered': field_count,
    'data': p_data
  })
    

@vendor_login_reqired
def add_product(request):
  ven_type = request.session.get('ven_type')
  ven_id = request.session.get('vendor_id')
  id = Vendor.objects.get(vendor_id = ven_id)
  
  if request.method == "POST":
    p_name = request.POST.get('productname')
    p_category = request.POST.get('type')
    p_specs = request.POST.get('specs')
    p_price = request.POST.get('price')
    p_stock = request.POST.get('stock')
    p_desc = request.POST.get('desc')
    p_image = request.FILES.get('images')
    p_video = request.FILES.get('video')
    
    product_save = Products(product_name = p_name ,product_type = p_category,product_specs = p_specs ,product_price = p_price, product_stock = p_stock, product_status = "N/A", product_description = p_desc, product_image = p_image, product_video = p_video, vendor = id) 
    
    product_save.save()
    return redirect('add_product')
  return render(request, "add_products.html", { "vendor_type": ven_type })


@vendor_login_reqired
def update_products(request, id):
  ven_type = request.session.get('ven_type')
  update = Products.objects.get(product_id = id)
  if request.method == "POST":
    update.product_name = request.POST.get('name')
    update.product_specs = request.POST.get('specs')
    update.product_type = request.POST.get('type')
    update.product_price = request.POST.get('price')
    update.product_stock = request.POST.get('stock')
    update.product_description = request.POST.get('desc')
    if request.FILES.get('image'):
      update.product_image = request.FILES.get('image')
    if request.FILES.get('video'):
      update.product_video = request.FILES.get('video')
    
    update.save()
    return redirect('manage')
  return render(request, 'update_products.html', {'data': update, 'vendor_type' : ven_type})

@vendor_login_reqired
def delete_products(request, id):
  try:
    del_product = Products.objects.get(product_id = id)
    del_product.delete()
    messages.success(request, "Product Successfully deleted")
    return redirect('manage')
  except Products.DoesNotExist:
    messages.error(request, "Product details does not exist")
  return render(request, 'product_manage.html')