from django.contrib import admin

from friends.models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('id', 'user', 'get_friends', 'get_notifications')

    def get_friends(self, obj):
        return ", ".join([friend.username for friend in obj.friends.all()])
    get_friends.short_description = "Friends"

    def get_notifications(self, obj):
        return ", ".join([str(notification) for notification in obj.notifications.all()])
    get_notifications.short_description = "Notifications"

# Register the model
admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver','is_active']
    search_fields = ['sender__username', 'receiver__username']
    # readonly_fields = ['id',]

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)
