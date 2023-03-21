from channels.routing import ProtocolTypeRouter, URLRouter
import django
import os
from django.core.asgi import get_asgi_application
from transactions.middlewares.middleware import TokenAuthMiddleware
from transactions.routing import websocket_urlpatterns as transaction_ws
from users.routing import websocket_urlpatterns as user_ws

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

websocket_urlpatterns =transaction_ws
websocket_urlpatterns+=user_ws

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})