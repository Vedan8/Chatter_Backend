# Chatter/asgi.py
import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Chatter.settings")

# 🔥 THIS IS THE MISSING LINE
django.setup()

# imports AFTER django.setup()
from chat.routing import websocket_urlpatterns
from chat.middleware import JwtCookieAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtCookieAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
