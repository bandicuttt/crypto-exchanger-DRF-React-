import os
from datetime import datetime

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import jwt
from config.settings import SIMPLE_JWT
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.db import close_old_connections
from django.contrib.auth import get_user_model


User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, key=SIMPLE_JWT['SIGNING_KEY'], algorithms=SIMPLE_JWT['ALGORITHM'])
    except Exception as e:
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        return AnonymousUser()

    try:
        user = User.objects.filter(id=payload['user_id']).first()
    except User.DoesNotExist:
        return AnonymousUser()
    return user


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
