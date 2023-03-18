from transactions.models.assets import Asset
from transactions.models.orders import Order
from django.contrib.auth import get_user_model
from transactions.serializers.orders import OrderSerializer
from asgiref.sync import sync_to_async
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from users.serializers.users import UserSerializer

import asyncio


User = get_user_model()

class GetOrdersConsumer(GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    order_serializer_class = OrderSerializer

    async def connect(self):
        user = await self.get_user()
        await self.accept()
        if user.is_authenticated:
            user = self.serializer_class(user).data
            initial_order_count = await self.get_order_count(user)
            data = await self.get_orders(user)
            for order in data:
                await self.send_json({
                    'messageType': 9,
                    'message': {
                        'messageText': 'GetOrder',
                        'order' : order,
                    }  
                })
            while True:
                await asyncio.sleep(5)
                order_count = await self.get_order_count(user)
                if order_count != initial_order_count:
                    initial_order_count = order_count
                    data = await self.get_last_order(user)
                    await self.send_json({
                        'messageType': 9,
                        'message': {
                            'messageText': 'GetOrder',
                            'order': data,
                        }
                    })
        else:
            await self.send_json({
                    'messageType': 6,
                    'message': {
                        'messageText': 'ErrorInfo', 
                        'reason': 'Not authorized',
                    }
                })

    @sync_to_async
    def get_user(self):
        return self.scope['user']
    
    @database_sync_to_async
    def get_orders(self, user):
        queryset = Order.objects.filter(user=user['id']).all()
        serializer = OrderSerializer(instance=queryset, many=True)
        return serializer.data
    
    @database_sync_to_async
    def get_last_order(self, user):
        queryset = Order.objects.filter(user=user['id']).last()
        serializer = OrderSerializer(instance=queryset)
        return serializer.data

    @database_sync_to_async
    def get_order_count(self, user):
        return Order.objects.filter(user=user['id']).count()



@receiver(post_save, sender=Asset)
def asset_saved(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'asset_%s' % instance.pk,
        {
            'type': 'asset_update',
            'current_price': instance.current_price
        }
    )

