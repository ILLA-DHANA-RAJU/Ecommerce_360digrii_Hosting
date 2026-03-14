import os
from django.db.models.signals import post_delete
from .models import Vendor,Products,Customer,Feedback
from django.dispatch import receiver


@receiver(post_delete, sender=Products)
def delete_product_files(sender, instance, **kwargs):
  if instance.product_image:
    image_path = instance.product_image.path
    if os.path.isfile(image_path):
      os.remove(image_path)
      
  if instance.product_video:
    video_path = instance.product_video.path
    if os.path.isfile(video_path):
      os.remove(video_path)
      
@receiver(post_delete, sender=Feedback)
def delete_feedback_files(sender, instance, **kwargs):
  if instance.feedback_image:
    image_path = instance.feedback_image.path
    if os.path.isfile(image_path):
      os.remove(image_path)
      
  if instance.feedback_video:
    video_path = instance.feedback_video.path
    if os.path.isfile(video_path):
      os.remove(video_path)
      
@receiver(post_delete, sender=Vendor)
def delete_vendor_files(sender, instance, **kwargs):
  if instance.image:
    image_path = instance.image.path
    if os.path.isfile(image_path):
      os.remove(image_path)

      
@receiver(post_delete, sender=Customer)
def delete_customer_files(sender, instance, **kwargs):
  if instance.image:
    image_path = instance.umage.path
    if os.path.isfile(image_path):
      os.remove(image_path)
