from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("***----------connect")
        print("***------user----",self.scope["user"])
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f"room_{self.room_name}"
            print("room name-----",self.room_group_name)

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Notify others in the room about the new participant
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_joined',
                    'username': self.scope["user"].username
                }
            )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify others in the room about the user leaving
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'username': self.scope["user"].username
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print('data------',data)
        action = data.get('action')
        print('actoin------',action)

        if action == 'send_signal':
            # Forward signaling data to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'signal_message',
                    'username': data['username'],
                    'signal_data': data['signal_data']
                }
            )

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            'action': 'user_joined',
            'username': event['username']
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'action': 'user_left',
            'username': event['username']
        }))

    async def signal_message(self, event):
        await self.send(text_data=json.dumps({
            'action': 'signal_message',
            'username': event['username'],
            'signal_data': event['signal_data']
        }))
