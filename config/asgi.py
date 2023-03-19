from channels.routing import ProtocolTypeRouter, URLRouter
import django
import os
from django.core.asgi import get_asgi_application
from transactions.middlewares.middleware import TokenAuthMiddleware
from transactions.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

