from django.urls import path
from globalchat import consumers

websocket_urlpattern=[
    path('ws/chat/<str:room_name>/',consumers.ChatConsumer.as_asgi()),
]