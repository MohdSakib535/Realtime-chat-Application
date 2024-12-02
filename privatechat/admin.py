from django.contrib import admin
from privatechat.models import PrivateChatRoom
# Register your models here.

class privatechatAdmin(admin.ModelAdmin):
    # list_filter = ['sender', 'receiver']
    list_display = ['user1', 'user2','is_active']
    class Meta:
        model = PrivateChatRoom

admin.site.register(PrivateChatRoom, privatechatAdmin)

