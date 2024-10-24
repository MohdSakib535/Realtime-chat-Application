# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name  = self.scope['url_route']['kwargs']['room_name']
#         print(self.room_name )
#         self.room_groups_name = f'chat_{self.room_name}'

#         print('channel name-----', self.channel_name)
#         print('group name--------',self.room_groups_name)

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_groups_name,
#             self.channel_name
#         )

#         await self.accept()

#         # Notify the group that a new user has joined
#         await self.channel_layer.group_send(
#             self.room_groups_name,
#             {
#                 'type': 'user_join',
#                 'user_id': self.scope['user'].id,
#                 'user_name': self.scope['user'].username,
#             }
#         )

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_groups_name,
#             self.channel_name
#         )

#         # Notify the group that a user has left
#         await self.channel_layer.group_send(
#             self.room_groups_name,
#             {
#                 'type': 'user_leave',
#                 'user_id': self.scope['user'].id,
#                 'user_name': self.scope['user'].username,
#             }
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         print('------',data)
#         message = data['message']
#         user_id = self.scope['user'].id
#         print('userid--------',user_id)
#         user_name = self.scope['user'].username
#         print('user_name--------',user_name)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_groups_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'user_id': user_id,
#                 'user_name': user_name,
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         user_id = event['user_id']
#         user_name = event['user_name']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'user_id': user_id,
#             'user_name': user_name,
#         }))

#     # Receive user join notification
#     async def user_join(self, event):
#         user_id = event['user_id']
#         user_name = event['user_name']

#         # Notify WebSocket about the new user
#         await self.send(text_data=json.dumps({
#             'message': f'{user_name} (ID: {user_id}) has joined the chat.',
#             'type':'user_join'
#         }))

#     # Receive user leave notification
#     async def user_leave(self, event):
#         user_id = event['user_id']
#         user_name = event['user_name']

#         # Notify WebSocket about the user leaving
#         await self.send(text_data=json.dumps({
#             'message': f'{user_name} (ID: {user_id}) has left the chat.',
#             'system': True,
#         }))


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import PublicRoomChatMessage, PublicChatRoom
from useraccount.models import CustomUser
from channels.db import database_sync_to_async  # Use sync_to_async for database operations

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Only allow connection if the user is authenticated
        if self.scope['user'].is_anonymous:
            await self.close()  # Close the WebSocket if the user is not authenticated
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Get or create the chat room asynchronously
        self.room = await self.get_chat_room(self.room_name)

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Notify the group that a new user has joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'user_id': self.scope['user'].id,
                'user_name': self.scope['user'].username,
            }
        )

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify the group that a user has left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'user_id': self.scope['user'].id,
                'user_name': self.scope['user'].username,
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        if self.scope['user'].is_anonymous:
            return  # Do not allow non-authenticated users to send messages

        data = json.loads(text_data)
        message = data['message']
        user_id = self.scope['user'].id
        user_name = self.scope['user'].username

        # Save the message to the database asynchronously
        timestamp= await self.save_message(user_id, message)


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'user_name': user_name,
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('event------',event)
        message = event['message']
        user_id = event['user_id']
        user_name = event['user_name']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'user_name': user_name,
            'timestamp': timestamp,
        }))

    # Receive user join notification
    async def user_join(self, event):
        user_id = event['user_id']
        user_name = event['user_name']

        # Notify WebSocket about the new user
        await self.send(text_data=json.dumps({
            'message': f'{user_name} (ID: {user_id}) has joined the chat.',
            'type': 'user_join'
        }))

    # Receive user leave notification
    async def user_leave(self, event):
        user_id = event['user_id']
        user_name = event['user_name']

        # Notify WebSocket about the user leaving
        await self.send(text_data=json.dumps({
            'message': f'{user_name} (ID: {user_id}) has left the chat.',
            'type': 'user_leave'
        }))


    @database_sync_to_async
    def get_chat_room(self, room_name):
        """
        Retrieves or creates a PublicChatRoom by room name.
        This is now asynchronous using `sync_to_async`.
        """
        return PublicChatRoom.objects.get_or_create(title=room_name)[0]

    @database_sync_to_async
    def save_message(self, user_id, message):
        """
        Saves a chat message to the database asynchronously.
        """
        user = CustomUser.objects.get(id=user_id)
        room = PublicChatRoom.objects.get(title=self.room_name)

        chat_message = PublicRoomChatMessage.objects.create(
            user=user,
            room=room,
            content=message,
            timestamp=timezone.now()
        )
        return chat_message.timestamp

