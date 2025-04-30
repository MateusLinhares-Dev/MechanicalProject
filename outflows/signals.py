from django.db.models.signals import post_save
from django.dispatch import receiver
from outflows.models import Outflows

@receiver(post_save, sender=Outflows)
def update_outflow(sender, instance, created,**kwargs):
    if created:
        quantity_inflow = instance.quantity
        product = instance.product
        
        
        if isinstance(quantity_inflow, int):
            product.quantity -= quantity_inflow
        
            product.save()