from django.urls import path
from privatechat import consumers

websocket_urlpattern=[
    path('ws/private/chat/<int:other_user>/',consumers.privateChatConsumer.as_asgi()),
]