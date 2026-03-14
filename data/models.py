from django.db import models
from django.core.validators import FileExtensionValidator
from django_resized import ResizedImageField


class Customer(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=50)
    mobileno = models.CharField(unique=True, max_length=15)
    alternate_mobileno = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300)
    zipcode = models.IntegerField()
    image = ResizedImageField(upload_to='customer_images/', force_format="PNG", blank=True, null=True)
    user_password = models.CharField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customer"


class Vendor(models.Model):
    vendor_id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=50)
    mobileno = models.CharField(unique=True, max_length=15)
    image = ResizedImageField(upload_to='vendor_images/', force_format="PNG", blank=True, null=True)
    vendor_type = models.CharField(max_length=50, blank=True, null=True)
    vendor_password = models.CharField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendor"


class Products(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_specs = models.CharField(max_length=400, blank=True, null=True)
    product_type = models.CharField(max_length=50)
    product_price = models.BigIntegerField()
    product_stock = models.BigIntegerField()
    product_status = models.CharField(max_length=20)
    product_description = models.TextField()
    product_image = ResizedImageField(upload_to='product_images/', force_format="PNG", blank=True, null=True)
    product_video = models.FileField(upload_to='product_videos/', validators=[FileExtensionValidator(['mp4'])], blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
        db_table = "products"


class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    order_amount = models.BigIntegerField()
    order_status = models.CharField(max_length=20, blank=True, null=True)
    payment_type = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=150, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=250, blank=True, null=True)
    shipping_address = models.CharField(max_length=400)
    cancel_reason = models.TextField(blank=True, null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"


class Feedback(models.Model):
    feedback_id = models.BigAutoField(primary_key=True)
    feedback_message = models.CharField(max_length=300, blank=True, null=True)
    feedback_image = ResizedImageField(upload_to='feedback_images/', force_format="PNG", blank=True, null=True)
    feedback_video = models.FileField(upload_to='feedback_videos/', validators=[FileExtensionValidator(['mp4'])], blank=True, null=True)

    feedback_date = models.DateTimeField(auto_now_add=True)

    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        db_table = "feedback"


class Search(models.Model):
    search_id = models.BigAutoField(primary_key=True)
    search_data = models.CharField(max_length=200, blank=True, null=True)
    search_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        db_table = "search"