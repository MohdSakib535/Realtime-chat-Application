from django.urls import path
from privatechat import views


urlpatterns=[
    path("private/chat/room",views.Private_chat,name="private_chat_room"),
    path('api/chatrooms/', views.PrivateChatRoomListView.as_view(), name='chatroom-list'),
    path('chat/messages/<int:other_user>/', views.RoomChatMessageListView.as_view(), name='chat-messages'),
    

]