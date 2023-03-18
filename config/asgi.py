from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django
import os
from django.core.asgi import get_asgi_application
from transactions.middlewares.middleware import TokenAuthMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from transactions.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
