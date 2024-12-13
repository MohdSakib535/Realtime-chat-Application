from django.urls import re_path,path
from . import consumers

websocket_urlpatterns_video = [
    # re_path(r'ws/video_call/(?P<room_name>\w+)/$', consumers.VideoCallConsumer.as_asgi()),
    path('ws/videoCall/<str:room_name>/',consumers.VideoCallConsumer.as_asgi())
]
