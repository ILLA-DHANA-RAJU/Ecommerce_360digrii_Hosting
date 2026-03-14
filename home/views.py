from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncDay
from data.models import Products, Orders
from home.decorators import vendor_login_reqired

# Create your views here.
def Home(request):
  fetch_data = Products.objects.all()
  return render(request, "home.html", {"fetch": fetch_data, "template_name": "home.html" })

def custome_page(request):
  return render(request, 'custome_login.html', {'hidden_search': True})

# vendor dashboard details code
@vendor_login_reqired
def dashboard(request):
  ven_id = request.session.get('vendor_id')
  pc = Products.objects.filter(vendor_id = ven_id).count()
  total_orders = Orders.objects.filter(vendor = ven_id).count()
  completed_orders = Orders.objects.filter(vendor = ven_id, payment_status = 'PAID')
  
  total_revenue = completed_orders.aggregate(total=Sum('order_amount'))['total'] or 0
  
  pending_orders = Orders.objects.filter(vendor = ven_id, order_status__in = ['PENDING' , 'PACKED' , 'SHIPPING', \
                                           'SHIPPED', 'OUT OF DELIVERY']).count()
  
  delivered_orders = Orders.objects.filter(vendor = ven_id, order_status = "DELIVERED").count()
  
  daily_data = Orders.objects.filter(vendor = ven_id).annotate(day = TruncDay('create_at')).values('day').annotate(total= Sum('order_amount')).order_by('day')
  
  days = [m['day'].strftime('%b %Y') for m in daily_data]
  revenues = [float(m['total']) for m in daily_data]
    
  context = {
    "proc" : pc,
    "ord" : total_orders,
    'delivered': delivered_orders,
    "revenue" : total_revenue,
    "pending" : pending_orders,
    "delivered" : delivered_orders,
    'days' : days,
    "revenues" : revenues
  }
  
  return render(request, 'dashboard.html', context)