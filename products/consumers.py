import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona o consumidor ao grupo de alertas de estoque e veículos
        await self.channel_layer.group_add('stock_alerts', self.channel_name)
        await self.channel_layer.group_add('vehicle_alerts', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove o consumidor dos grupos ao desconectar
        await self.channel_layer.group_discard('stock_alerts', self.channel_name)
        await self.channel_layer.group_discard('vehicle_alerts', self.channel_name)

    async def receive(self, text_data):
        # Processa mensagens recebidas do cliente (se necessário)
        try:
            data = json.loads(text_data)
            if 'action' in data:
                if data['action'] == 'acknowledge':
                    # Lógica para reconhecer notificações (implementação futura)
                    pass
        except json.JSONDecodeError:
            pass

    async def send_notification(self, event):
        # Envia notificações para o cliente
        await self.send(text_data=json.dumps({
            'type': event.get('alert_type', 'stock'),
            'notifications': event['notifications']
        }))
        
    async def send_vehicle_notification(self, event):
        # Envia notificações específicas de veículos
        await self.send(text_data=json.dumps({
            'type': 'vehicle',
            'notifications': event['notifications']
        }))