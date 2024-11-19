# friends/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import FriendRequest
from Notification.models import Notification

User = get_user_model()



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"notification_user_{self.scope['user'].id}"
            print('notif gp id-------',self.group_name)
            
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    async def notification(self, event):
        message = event['notification']
        print('mess-------',message)
        count = event.get('count', 0)

        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': message,
            'count': count,
        }))