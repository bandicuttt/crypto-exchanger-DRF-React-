from channels.generic.websocket import AsyncWebsocketConsumer
import json
import uuid
from asgiref.sync import sync_to_async
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from transactions.models.assets import Asset

class SubscribeMarketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.subscriptions = {}

    async def disconnect(self, close_code):
        for subscription_id, asset_id in dict(self.subscriptions).items():
            await self.unsubscribe(subscription_id, asset_id)
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('action')

        if message_type == 'SubscribeMarketData':
            asset_id = data.get('assetId')
            if asset_id:
                subscription_id = str(uuid.uuid4())
                await self.subscribe(subscription_id, asset_id)
                await self.send_success_info(subscription_id)
            else:
                await self.send_error_info('Missing assetId')
        elif message_type == 'UnsubscribeMarketData':
            subscription_id = data.get('subscriptionId')
            asset_id = self.subscriptions.get(subscription_id)
            if asset_id:
                await self.unsubscribe(subscription_id, asset_id)
            else:
                await self.send_error_info('Invalid subscriptionId')
        else:
            await self.send_error_info('Invalid message type')

    async def subscribe(self, subscription_id, asset_id):
        asset = await self.get_asset(asset_id)
        if asset:
            self.subscriptions[subscription_id] = asset_id
            await self.channel_layer.group_add(f'asset_{asset_id}', self.channel_name)
        else:
            await self.send_error_info('Invalid assetId')

    async def unsubscribe(self, subscription_id, asset_id):
        del self.subscriptions[subscription_id]
        await self.channel_layer.group_discard(f'asset_{asset_id}', self.channel_name)

    async def send_success_info(self, subscription_id):
        message = {
            'messageType': 5,
            'message': {
                'messageText' : 'SuccessInfo',
                'subscriptionId': subscription_id,
                }
            }
        await self.send(json.dumps(message))

    async def send_error_info(self, reason):
        message = {
            'messageType': 6,
            'message': {
                'messageText': 'ErrorInfo', 
                'reason': reason
                }
            }
        await self.send(json.dumps(message))

    async def send_market_data_update(self, asset_id, current_price):
        message = {
            'messageType': 8,
            'message': {
                'messageText': 'MarketDataUpdate',
                'assetId': asset_id,
                'currentPrice': current_price
                }
            }
        await self.send(json.dumps(message))

    async def get_asset(self, asset_id):
        try:
            return await sync_to_async(Asset.objects.get)(id=asset_id)
        except Asset.DoesNotExist:
            return None

    async def update_prices(self):
        assets = await Asset.objects.all()
        for asset in assets:
            current_price = asset.current_price
            previous_price = getattr(self, f'previous_price_{asset.id}', None)
            if previous_price is None or current_price != previous_price:
                await self.channel_layer.group_send(
                    f'asset_{asset.id}',
                        {
                            'type': 'market_data_update',
                            'current_price': str(current_price)
                        }
                    )
                setattr(self, f'previous_price_{asset.id}', current_price)

    async def market_data_update(self, event):
        current_price = event['current_price']
        await self.send_market_data_update(self.scope['url_route']['kwargs']['asset_id'], current_price)

    async def asset_update(self, event):
        current_price = event['current_price']
        await self.send(text_data=json.dumps({
            'messageType': 8,
            'message': {
                'messageText': 'MarketDataUpdate',
                'currentPrice': str(current_price)
                }
        }))


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