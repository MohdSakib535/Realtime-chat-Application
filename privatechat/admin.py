from django.contrib import admin
from privatechat.models import PrivateChatRoom,RoomChatMessage
# Register your models here.

class privatechatAdmin(admin.ModelAdmin):
    # list_filter = ['sender', 'receiver']
    list_display = ['id','user1', 'user2','is_active']
    class Meta:
        model = PrivateChatRoom

admin.site.register(PrivateChatRoom, privatechatAdmin)




class RoomChatMessageAdmin(admin.ModelAdmin):
    # list_filter = ['sender', 'receiver']
    list_display = ['user', 'room','content']
    class Meta:
        model = RoomChatMessage

admin.site.register(RoomChatMessage, RoomChatMessageAdmin)



