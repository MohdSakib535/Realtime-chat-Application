import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import PrivateChatRoom
from useraccount.models import CustomUser
from channels.db import database_sync_to_async 
from django.core.cache import cache

class privateChatConsumer(AsyncWebsocketConsumer):

    def get_room_name(self,user1_id, user2_id):
        """Generate a unique room name for two users."""
        sorted_ids = sorted([str(user1_id), str(user2_id)])
        return f"chat_{sorted_ids[0]}_{sorted_ids[1]}"


    async def connect(self):
        print("***********private chats**********")
        current_user=self.scope['user']
        self.current_user=self.scope['user']
        print('current_user-----',current_user.id)

        other_user=self.scope['url_route']['kwargs']['other_user']
        other_user_data=await self.other_user_details(other_user)
        print("other iuser---333--",(other_user_data))

        if current_user.is_anonymous:
            await self.close()
            
        self.room_name=self.get_room_name(other_user,current_user.id)
        print('room_name--con---',self.room_name)
      
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # Mark user as online
        # await self.set_user_online(self.current_user.id)


        
 
        #notify for status offline or online
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type':'user_status',
                'other_user':other_user_data,
                'status':'online'
            }
        )
        await self.accept()

    async def user_status(self,event):
        # print('event----5-----',event)
        await self.send(text_data=json.dumps({
            'type':event['type'],
            'status':event['status'],
            'other user':event['other_user']

        }))

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name

        )


    async def receive(self, text_data=None, bytes_data=None):
        
        # if current_user.is_anonymous:
        #     return
        print('text--------',text_data)
        data=json.loads(text_data)
        print(data)
        message=data.get('message')
        friend_id=data.get('friend_id')
        print('room_name--rec---',self.room_name)
        print('frie------',friend_id)

        await self.channel_layer.group_send(
            self.room_name,
            {   
                'type':'chat_messages',
                'message':message,
                'friendId':friend_id
            }

        )

    async def chat_messages(self,event):
        current_user=self.scope['user']
        print(current_user.id)
        print("mess---------",event)
        await self.send(text_data=json.dumps({
            'message':event['message'],
            'friend_data':{
                'type':'user_chat_message',
                'id': event['friendId'],
                # 'id': current_user.id,
            }
        }))


    
        
        
   
    # async def set_user_online(self, user_id):
    #     """
    #     Mark the user as online. If the user is already online (has active connections),
    #     increment the connection count.
    #     """
    #     key = f"user_{user_id}_connections"
    #     current_connections = cache.get(key, 0)
    #     cache.set(key, current_connections + 1, timeout=None)
        

    @database_sync_to_async
    def other_user_details(self,id):
        m1=CustomUser.objects.get(id=id)
        m2={
                'id': m1.id,
                'username': m1.username,
                # Add other necessary fields like avatar URL, etc.
            }
        print("m2-------",m2)
        return m2
        


