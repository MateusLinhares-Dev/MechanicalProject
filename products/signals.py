from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from collections import defaultdict

@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    products_low_stock = Product.objects.filter(quantity__lte=5).values()
    if products_low_stock:
        channel_layer = get_channel_layer()

        notifications = [
            {'message': {
                'name_product': product['name_product'],
                'quantity': product['quantity']
            }} for product in products_low_stock
        ]

        resultado = defaultdict(int)
        
        for item in notifications:
            nome = item['message']['name_product']
            quantidade = item['message']['quantity']
            resultado[nome] += quantidade

        async_to_sync(channel_layer.group_send)(
            'stock_alerts',
            {
                'type': 'send_notification',
                'notifications': [
                    {'message': {'name_product': nome, 'quantity': quantidade}}
                    for nome, quantidade in resultado.items()
                ]
            }
        )