from django.shortcuts import render, redirect
from .models import Orders, Products, Feedback
from django.contrib import messages

# Create your views here.
def feedback_page(request, id):
  try:
    order = Orders.objects.get(order_id = id)
    product = order.product
  except Orders.DoesNotExist:
    messages.error(request, "Order details not avalible ")
    return redirect('orders')
  
  if request.method == "POST":
    product_id = request.POST.get('pro_id')
    feedback_msg = request.POST.get('feedmsg')
    feedback_img = request.POST.get('image')
    feedback_vd = request.POST.get('video')
    
    feedback = Feedback(
      order = order,
      product = product,
      feedback_message = feedback_msg,
      feedback_image = feedback_img,
      feedback_video = feedback_vd,
    )
    feedback.save()
    messages.success(request, "Thank You For Your FeedBack 🤩!")
    return redirect('orders')
  return render(request, "feedback.html", {"res": order})

