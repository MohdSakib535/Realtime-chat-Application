
# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from friends.models import FriendRequest
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from Notification.models import Notification

User = get_user_model()

class FriendRequestConsumer(AsyncWebsocketConsumer):
   
    async def connect(self):
        print('inside notification app-**********************')
        print("FriendRequestConsumer: Connection attempt.")
        user = self.scope["user"]
        if user.is_anonymous:
            print("FriendRequestConsumer: Anonymous user. Connection closed.")
            await self.close()
        else:
            # Join friend request group based on user ID
            self.friend_request_group_name = f"friend_request_user_{user.id}"
            await self.channel_layer.group_add(
                self.friend_request_group_name,
                self.channel_name
            )
            # Join general notification group
            self.notification_group_name = f"notification_user_{user.id}"
            await self.channel_layer.group_add(
                self.notification_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"FriendRequestConsumer: User {user.id} connected and joined groups.")

    async def disconnect(self, close_code):
        # Leave friend request group
        await self.channel_layer.group_discard(
            self.friend_request_group_name,
            self.channel_name
        )
        # Leave notification group
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )
        print("FriendRequestConsumer: Disconnected and left groups.")

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print('FriendRequestConsumer: Received data:', data)
        
        if data.get('type') == 'send_request':
            target_user_id = data.get('target_user_id')
            print('FriendRequestConsumer: Target User ID:', target_user_id)
            
            sender = self.scope['user']
            print('FriendRequestConsumer: Sender ID:', sender.id)

            # Prevent sending request to self
            if sender.id == target_user_id:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': "You cannot send a friend request to yourself."
                }))
                return

            try:
                target_user = await database_sync_to_async(User.objects.get)(id=target_user_id)
                print(f"FriendRequestConsumer: Target User fetched: {target_user.username}")
            except User.DoesNotExist:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': "Target user does not exist."
                }))
                return

            # Check if FriendRequest already exists
            existing_request = await self.check_existing_request(sender.id, target_user_id)
            if existing_request:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': "Friend request already sent."
                }))
                return

            # Create FriendRequest
            await self.create_friend_request(sender.id, target_user_id)
            print(f"FriendRequestConsumer: Friend request created from {sender.username} to {target_user.username}")

            # Notify the target user via their friend request group
            await self.channel_layer.group_send(
                f"friend_request_user_{target_user_id}",
                {
                    'type': 'friend_request',
                    'message': f"{sender.username} has sent you a friend request.",
                    'sender_user': {
                        'id': sender.id,
                        'username': sender.username,
                        'email': sender.email,
                        'profile_picture': sender.profile_image.url if sender.profile_image else '',  
                    },
                    'receiver_user': { 
                        'id': target_user.id,
                        'username': target_user.username,
                        'email': target_user.email,
                        'profile_picture': target_user.profile_image.url if target_user.profile_image else '',
                    },
                }
            )
            print(f"FriendRequestConsumer: Notification sent to group friend_request_user_{target_user_id}")

            count_notification=  await self.get_unread_notification_count(target_user_id)
            print('-------',count_notification)

            # Additionally, send a general notification
            await self.channel_layer.group_send(
                f"notification_user_{target_user_id}",
                {
                    'type': 'notification',
                    'count':count_notification,
                    'notification': f"{sender.username} has sent you a friend request."
                }
            )
            print(f"FriendRequestConsumer: General notification sent to group notification_user_{target_user_id}")

    # Handler for friend_request messages
    async def friend_request(self, event):
        print('FriendRequestConsumer: Handling friend_request event:', event)
        message = event['message']
        sender = event['sender_user']
        receiver = event['receiver_user'] 

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message,
            'sender': sender,
            'receiver': receiver  
        }))
        print(f"FriendRequestConsumer: Sent friend_request message to WebSocket for user {receiver['id']}")

    # Handler for general notifications
    async def notification(self, event):
        print('FriendRequestConsumer: Handling notification event:', event)
        notification = event['notification']

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
        print(f"FriendRequestConsumer: Sent notification message to WebSocket.")

    @database_sync_to_async
    def check_existing_request(self, from_user_id, to_user_id):
        exists = FriendRequest.objects.filter(sender_id=from_user_id, receiver_id=to_user_id, is_active=True).exists()
        print(f"FriendRequestConsumer: Existing request check: {exists}")
        return exists

    @database_sync_to_async
    def create_friend_request(self, from_user_id, to_user_id):
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
        friend_request = FriendRequest.objects.create(sender=from_user, receiver=to_user, is_active=True)
        print(f"FriendRequestConsumer: FriendRequest created: {friend_request}")
        return friend_request
    
    @database_sync_to_async
    def get_unread_notification_count(self,id):
        print('notification id------',id)
        unread=Notification.objects.filter(target_id=id).count()
        print("l--------",unread)
        return unread





