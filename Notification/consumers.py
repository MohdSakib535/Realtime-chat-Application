# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from friends.models import FriendRequest
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from useraccount.models import CustomUser

class FriendRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
        else:
            # Join room group based on user ID
            self.group_name = f"user_{user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print('data------',data)
        if data['type'] == 'send_request':
            target_user_id = data['target_user_id']
            # print('sefl------',self.scope)
            sender = self.scope['user']
            print('sender------',sender)

            # Prevent sending request to self
            if sender.id == target_user_id:
                await self.send(text_data=json.dumps({
                    'message': "You cannot send a friend request to yourself."
                }))
                return
            
            
            target_user = await database_sync_to_async(CustomUser.objects.get)(id=target_user_id)

            # Check if FriendRequest already exists
            # existing_request = await self.check_existing_request(sender.id, target_user_id)
            # if existing_request:
            #     await self.send(text_data=json.dumps({
            #         'message': "Friend request already sent."
            #     }))
            #     return

            # Create FriendRequest

            await self.create_friend_request(sender.id, target_user_id)

            # Notify the target user via their group
            await self.channel_layer.group_send(
                f"user_{target_user_id}",
                {
                    'type': 'friend_request',
                    'message': f"{sender.username} has sent you a friend request.",
                    'sender_user': {
                        'id': sender.id,
                        'username': sender.username,
                        'email': sender.email,
                        'profile_picture': sender.profile_image.url if sender.profile_image else '',  # Assuming profile_picture is a field in User
                    },
                    'reciever_user':{
                        'id': target_user.id,
                        'username': target_user.username,
                        'email': target_user.email,
                        'profile_picture': target_user.profile_image.url if target_user.profile_image else '',  # Assuming profile_picture is a field in User
                    },
                }
            )

    # Receive message from group
    async def friend_request(self, event):
        print('mdff------',event)
        message = event['message']
        sender=event['sender_user']
        reciever=event['reciever_user']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':event['type'],
            'message': message,
            'sender':sender,
            'reviever':reciever
        }))

    # @database_sync_to_async
    # def check_existing_request(self, from_user_id, to_user_id):
    #     return FriendRequest.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).exists()

    @database_sync_to_async
    def create_friend_request(self, from_user_id, to_user_id):
        from_user_id=CustomUser.objects.get(id=from_user_id)
        to_user_id=CustomUser.objects.get(id=to_user_id)
        return FriendRequest.objects.create(sender=from_user_id, receiver=to_user_id)
