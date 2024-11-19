from django.urls import re_path,path
from Notification import consumers

websocket_urlpatterns_notification = [
    path('ws/friend-requests/',consumers.FriendRequestConsumer.as_asgi()),
]