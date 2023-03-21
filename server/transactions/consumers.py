from transactions.models.assets import Asset
from transactions.models.orders import Order
from django.contrib.auth import get_user_model
from transactions.serializers.assets import AssetSerializer
from transactions.serializers.orders import OrderSerializer
from asgiref.sync import sync_to_async
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from users.serializers.users import UserSerializer
from django.db.models.signals import post_save
import asyncio


User = get_user_model()


class AssetConsumer(GenericAsyncAPIConsumer):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    async def asset_saved_handler(self, event):
        asset = event['instance']
        await self.send_json({
                'messageType': 10,
                'message': {
                    'messageText': 'GetAsset',
                    'order' : AssetSerializer(asset).data,
                }
            })
    
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            f"asset_monitor",
            self.channel_name,
        )
        data = await self.get_all_assets()
        for asset in data:
            await self.send_json({
                'messageType': 10,
                'message': {
                    'messageText': 'GetAsset',
                    'asset' : asset,
                }  
            })
        await database_sync_to_async(post_save.connect)(asset_saved, sender=Asset)
        
    
    @database_sync_to_async
    def get_all_assets(self):
        queryset = Asset.objects.all()
        serializer = AssetSerializer(instance=queryset, many=True)
        return serializer.data


class GetOrdersConsumer(GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    order_serializer_class = OrderSerializer

    async def order_saved_handler(self, event):
        order = event['instance']
        user = await self.get_user()
        if order.user.id == user.id:
            await self.send_json({
                'messageType': 9,
                'message': {
                    'messageText': 'GetOrder',
                    'order' : OrderSerializer(order).data,
                }
            })

    async def connect(self):
        user = await self.get_user()
        await self.accept()
        if user.is_authenticated:
            await self.channel_layer.group_add(
                f"user-{user.id}",
                self.channel_name,
            )
            user = self.serializer_class(user).data
            data = await self.get_orders(user)
            await self.send_json({
                'messageType': 9,
                'message': {
                    'messageText': 'GetOrder',
                    'orders' : data,
                }  
            })
            await database_sync_to_async(post_save.connect)(order_saved, sender=Order)
        else:
            await self.send_json({
                    'messageType': 6,
                    'message': {
                        'messageText': 'ErrorInfo', 
                        'reason': 'Not authorized',
                    }
                })
            await self.close()

    @sync_to_async
    def get_user(self):
        return self.scope['user']
    
    @database_sync_to_async
    def get_orders(self, user):
        queryset = Order.objects.filter(user=user['id']).all()
        serializer = OrderSerializer(instance=queryset, many=True)
        return serializer.data

@receiver(post_save, sender=Order)
def order_saved(sender, instance, created, **kwargs):
    if created:
        message_type = 'PlaceOrder'
    else:
        message_type = 'OrderUpdated'
    message = {
        'messageText': message_type,
        'order': OrderSerializer(instance).data,
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user-{instance.user.id}", 
        {
            'type': 'send_json',
            'message': message,
        }
    )

@receiver(post_save, sender=Asset)
def asset_saved(sender, instance, created, **kwargs):
    message = {
        'messageText': 'GetAsset',
        'asset': AssetSerializer(instance).data,
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"asset_monitor", 
        {
            'type': 'send_json',
            'message': message,
        }
    )







