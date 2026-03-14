"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from home import views as h1
from signup import views as v1
from login import views as v2
from contact import views as c1
from products import views as p1
from payment import views as p2
from search import views as s1
from cart import views as c2
from order import views as o1
from data import views as d1

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("", h1.Home, name="home"),
    path('custome/login/', h1.custome_page, name="custome_login"),
    path('dashboard/', h1.dashboard, name="dashboard"),
    
    path('signup/', v1.signup_view, name="signup"),
    path('update/details/<int:id>/', v1.update_customer, name="update"),
    path('delete/user/<int:id>/', v1.delete_customer, name="delete"),
    path('signin/', v1.vendor_signin, name="vendor_signin"),
    path('vendor/profile/', v1.vendor_profile, name="vendor_profile"),
    path('vendor/profile/update/<int:id>', v1.vendor_update, name="vendor_update"),
    path('vendor/profile/delete/<int:id>', v1.vendor_delete, name="vendor_delete"),
    
    path('login/', v2.login_view, name="login"),
    path('logout/', v2.user_logout, name="logout"),
    path('vendor/login/', v2.vendor_login, name="vendor_login"),
    path('vendor/logout/', v2.vendor_logout, name="vendor_logout"),
    
    path('contactus/', c1.contact, name="contact"), 
    path('aboutus/', c1.about, name="about"),
    
    path('feedback/page/<int:id>', d1.feedback_page, name="feedback"),
    
    path('products/', p1.products_data, name="product"),
    path('product/page/<int:id>/<str:category>', p1.product_details, name="product_details"),
    path('vendor/products/manage/', p1.product_manage, name="manage"),
    path('api/', p1.api_manage, name="api_product_data"),
    path('vendor/add_product/', p1.add_product, name="add_product"),
    path('update/products/<int:id>/', p1.update_products, name="update_products"),
    path('delete/products/<int:id>/', p1.delete_products, name="delete_products"),
    
    path('profile/', v1.profile, name="profile"),
    
    # path('search/', s1.search_details, name="search"),
    path("api/product/", s1.api_products, name="api_fetch"),
    path('api/orders/', s1.api_orders, name="api_orders"),
    
    path('cart/', c2.cart_data, name="cart"),
    path('add/', c2.add_list, name="add_list"),
    path('remove/', c2.remove_list, name="remove_item"),
    path('cartlist/', c2.cart_page, name="cart_add"),
    
    path('cart/list/', c2.show_cart, name="cart_show"),
    path('product/add/cart/<int:id>/', c2.add_cart, name="add_cart"),
    path('product/remove/cart/<int:id>/', c2.rm_cart, name="remove_cart"),
    path('product/cart/incr/<int:id>/', c2.incr_pro, name="increment_pro"),
    path('product/dcr/cart/<int:id>/', c2.dcr_pro, name="decrement_pro"),
    
    path('orders/', o1.orders, name="orders"),
    path('order/details/<int:id>/', o1.order_details, name="order_details"),
    path('orders/data/', o1.manage_orders, name="manage_orders"),
    path('api/order/manage', o1.api_order_manage, name='api_order_manage'),
    path('api/update/order/ajax/', o1.api_order_update, name="api_order_update"),
    path('order/cancel/page/<int:id>', o1.cancel_page, name="cancel_page"),
    path('order/cancel/<int:o_id>/', o1.ord_cancel, name="cancel"),
    path('order/invioce/page/<int:id>', o1.invoice, name="invoice_page"),
    path('invioce/download/<int:id>', o1.download_invioce, name='download'),
    
    path('deliver/address/<int:id>/', p2.deliver_add, name="deliver_add"),
    path('order/confirm/', p2.payment_page, name="payment_page"),
    path('payment/resume/<int:id>', p2.resume_payment, name="resume_payment"),
    path('payment/success/', p2.payment_success, name="payment_success"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
