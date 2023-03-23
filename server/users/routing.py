from django.urls import path, re_path

from transactions.consumers import GetOrdersConsumer, AssetConsumer
from users.consumers import SubscribeMarketConsumer


websocket_urlpatterns = [
   path('ws/subscribe-market/', SubscribeMarketConsumer.as_asgi()),
]