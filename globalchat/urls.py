from django.urls import path
from globalchat import views

urlpatterns=[
    path("pu",views.Public_chat,name='public_url'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),

]