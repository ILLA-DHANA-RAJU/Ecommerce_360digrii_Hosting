from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from data.models import Products, Orders
from home.decorators import customer_login_required, vendor_login_reqired
from django.views.decorators.http import require_POST
from django.contrib import messages
from xhtml2pdf import pisa
from django.template.loader import get_template

#customer order item details showing
@customer_login_required
def orders(request):
  c_id = request.session.get('customer_id')
  or_details = Orders.objects.filter(user = c_id) 
  return render(request, "orders.html", {'ord': or_details})

@customer_login_required
def order_details(request, id):
  item = Orders.objects.get(order_id = id)
  return render(request, "order_page.html", {"ord": item})


#vendor order manage
@vendor_login_reqired
def manage_orders(request):
  return render(request, 'vendor_order_manage.html')

def api_order_manage(request):  
  vendor_id = request.session.get('vendor_id')
  order_status = request.GET.get('order_status')
  payment_type = request.GET.get('payment_type')
  # vendor = Orders.objects.filter(vendor = vendor_id)
  
  draw = int(request.GET.get('draw', 1))
  start = int(request.GET.get('start', 0))
  length = int(request.GET.get('length', 10))
  search_data = request.GET.get("search[value]", "")
  order_columns = int(request.GET.get('order[0][column]', 0))
  order_dir = request.GET.get('order[0][dir]', 'desc')
  
  columns = ['order_id', 'product__product_name' ,'order_amount', 'quantity', 'order_status', 'payment_type', 'payment_status']
  
  order_field = columns[order_columns]
  if order_dir == 'desc':
    order_field = '-' + order_field
  
  qr = Orders.objects.filter(vendor = vendor_id)
  if search_data:
    qr = qr.filter(Q(payment_type__icontains = search_data) 
                 | Q(order_amount__icontains = search_data) 
                 | Q(product__product_name__icontains = search_data) 
                 | Q(order_id__icontains = search_data) 
                 | Q(payment_status__icontains = search_data) 
                 | Q(order_status__icontains = search_data)) 
  
  if order_status:
    qr = qr.filter(order_status = order_status)
    
  if payment_type:
    qr = qr.filter(payment_type__iexact = payment_type)
     
  total_count = Orders.objects.filter(vendor = vendor_id).count()
  field_count = qr.count()
  
  qr = qr.order_by(order_field)[start:start+length]
  
  p_data =[]
  si = start + 1
  
  for q in qr:
    p_data.append({
      'si' : si,
      'name' : q.product.product_name,
      'stock': q.quantity,
      'price': q.order_amount,
      'status': q.order_status,
      'payment_type' : q.payment_type,
      'payment_status' : q.payment_status,
      'operations' : (
        f"""<button class='edit-btn' data-id='{q.order_id}'>Edit</button>
        <button class='save-btn' data-id='{q.order_id}' style='display:none'>Save</button> """  
      )  
    })
    si += 1

  return JsonResponse({
    'draw': draw,
    'recordsTotal': total_count,
    'recordsFiltered': field_count,
    'data': p_data
  })
  
  
# vendor order updates 
@require_POST
def api_order_update(request):
  
  order = Orders.objects.get(order_id = request.POST['order_id'])
  
  if order.payment_status == "PAID" and order.order_status == 'DELIVERED':
    return JsonResponse({'error': "Delivered & PAID orders cannot be modified"}, status=400)
  
  if order.order_status == "CANCELLED" and order.payment_status == 'CANCELLED':
    return JsonResponse({'error': "Order Cancelled by customer.Cann't change manually"}, status=400)
   
  order.order_status = request.POST['order_status']
  order.payment_status = request.POST['payment_status']
  order.save()
  
  return JsonResponse({"status": "ok"})


#order cancel message page
def cancel_page(req, id):
  order_id = Orders.objects.get(order_id = id)
  
  if not order_id:
    messages.error(req, "This is accessable")
    return redirect('order_details')

  if order_id.payment_status == "CANCELLED" or  order_id.order_status == "CANCELLED":
    messages.error(req, "Order Alread Cancelled")
    return redirect('order_details', id=order_id.order_id)
  
  return render(req, "order_cancel_page.html", {"order" : order_id})

# order cancel 
@customer_login_required
def ord_cancel(request, o_id):
  try:
    customer = request.session.get('customer_id')
    order = Orders.objects.get(order_id = o_id, user_id = customer)
    # product = Products.objects.get(product_id = p_id)
  
    product = order.product
    product.product_stock += order.quantity
    product.save()
    
    order.order_status = "CANCELLED"
    
    if order.payment_type == "online":
      order.payment_status = "CANCELLED"
      order.razorpay_order_id = "N/A"

    if request.method == "POST":
      reason = request.POST.get('reason')
      order.cancel_reason = reason
    
    order.payment_status = "CANCELLED"
    
    order.save()
    
    messages.success(request, "Order cancelled Successfully")
    return redirect('order_details', id=order.order_id)
  
  except Exception as e:
    messages.error(request, f"Something want wrong: {e}")
    return redirect('orders')
  
# invioce page code 
def invoice(request, id):
  order = get_object_or_404(Orders, order_id = id)
  
  if order.order_status == "CANCELLED":
    return redirect('orders')
  
  return render(request, "invoice.html", {"order": order})

# invioce donwload 
def download_invioce(request, id):
  order = get_object_or_404(Orders, order_id = id)
  
  temaplate = get_template('invoice.html')
  html = temaplate.render({"order": order})
  
  response = HttpResponse(content_type = "application/pdf")
  response["Content-Disposition"] = f'attachment; filename="invoice_{order.order_id}.pdf"'
  
  pisa.CreatePDF(html, dest=response)
  return response