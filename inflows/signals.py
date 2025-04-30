from django.db.models.signals import post_save
from django.dispatch import receiver
from inflows.models import Inflows
from products.models import Product

@receiver(post_save, sender=Inflows)
def update_inflow(sender, instance, created,**kwargs):
    if created:
        quantity_inflow = instance.quantity
        product = instance.product
        
        if isinstance(quantity_inflow, int):
            product.quantity += quantity_inflow
        
            product.save()