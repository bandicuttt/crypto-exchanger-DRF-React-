from django.urls import path, re_path

from transactions.consumers import GetOrdersConsumer, AssetConsumer
from users.consumers import SubscribeMarketConsumer


websocket_urlpatterns = [
    path("ws/orders/", GetOrdersConsumer.as_asgi()),
    path("ws/get-all-assets/", AssetConsumer.as_asgi()),
]