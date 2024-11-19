from django.urls import path
from privatechat import views


urlpatterns=[
    path("private/chat/room",views.Private_chat,name="private_chat_room")
    

]