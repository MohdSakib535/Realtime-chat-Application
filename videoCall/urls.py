from django.urls import path
from videoCall import views

app_name = "videoCall"

urlpatterns = [
    path("videoCall/<str:roomName>", views.base, name="room"),
    path("call/start/<int:user_id>/", views.start_video_call, name="start_call"),
    path("call/<int:call_id>/end/", views.end_video_call, name="end_call"),
    path("ad", views.add_user, name="add_user"),
    path('api/rooms/create/', views.RoomCreateAPIView.as_view(), name='room-create'),
]
