from Notification.serializers import Notification_serializers
from Notification.models import Notification
from rest_framework import viewsets
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notification_to_user(user_id, message):
    # Get the channel layer
    channel_layer = get_channel_layer()
    
    # Define the group name based on the user ID
    group_name = f"notifications_{user_id}"

    # Send a message to the group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "notification": message,
        }
    )


class Notification_list(viewsets.ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=Notification_serializers



from Notification.serializers import Notification_serializers
from rest_framework.response import Response

class mark_notifications_as_read(viewsets.ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=Notification_serializers

    def create(self,request,*args,**kwargs):
        notifications = Notification.objects.all()
        notifications.update(read=True)
        return Response('ok')



