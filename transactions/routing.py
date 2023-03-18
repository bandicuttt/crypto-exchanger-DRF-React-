from django.urls import path, re_path

from transactions.consumers import GetOrdersConsumer
from users.consumers import SubscribeMarketConsumer


websocket_urlpatterns = [
    path("ws/orders/", GetOrdersConsumer.as_asgi()),
    path('ws/subscribe-market/<int:asset_id>/', SubscribeMarketConsumer.as_asgi()),
]