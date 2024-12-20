"""
ASGI config for ChatApplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from Notification.routing import websocket_urlpatterns_notification as notification_chat_url
from globalchat.routing import websocket_urlpattern as public_chat_url
from friends.routing import websocket_urlpatterns as friend_related_url
from privatechat.routings import websocket_urlpattern as private_chat_url
from videoCall.routing import websocket_urlpatterns_video as video_call
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApplication.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
        public_chat_url+
        notification_chat_url+
        friend_related_url+
        private_chat_url+
        video_call
        
    )
    )
    
})
