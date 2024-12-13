from django.urls import path
from videoCall import views

urlpatterns=[
    path("videoCall/<str:roomName>",views.base,name='base'),
    path("ad",views.add_user,name='add_user'),
    path('api/rooms/create/', views.RoomCreateAPIView.as_view(), name='room-create'),

]