from django.shortcuts import render
from  useraccount.models import CustomUser
from friends.models import FriendList,FriendRequest
from Notification.models import Notification
from django.shortcuts import get_object_or_404
from privatechat.models import PrivateChatRoom
from django.db.models import Q,F,Case,When,IntegerField

from rest_framework import viewsets


def Private_chat(request):
    context={}
    current_user=request.user
    print('------',request.user)
    
    # friend_data=PrivateChatRoom.objects.filter(user2=request.user).all()

    friend_data=PrivateChatRoom.objects.filter(
        Q(user1=current_user)|Q(user2=current_user)
    ).annotate(
        other_user_id=Case(
            When(user1=current_user,then=F('user2_id')),
            When(user2=current_user,then=F('user1_id')),
            otehr_field=IntegerField()
        )
    )
    other_user_ids = friend_data.values_list('other_user_id', flat=True).distinct()
    print('otehr------',other_user_ids)
    friend_data3 = CustomUser.objects.filter(id__in=other_user_ids)
    print("--priv------",friend_data3)
    for i in friend_data3:
        print('---i----',i.username)


    

    context['friend_data']=friend_data3
    context['user_id']=request.user.id
    # return render(request,'private_chats.html',context)
    return render(request,'privatechats2.html',context)



"""
APi section
"""

from rest_framework.generics import ListAPIView
from .models import RoomChatMessage
from rest_framework import generics, permissions
from .serializers import PrivateChatRoomSerializer,RoomChatMessageSerializer
from rest_framework.permissions import IsAuthenticated

# class RoomChatMessageListView(ListAPIView):
#     """
#     API to retrieve chat messages for a specific room.
#     """
#     serializer_class = RoomChatMessageSerializer
#     permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     room_id = self.kwargs['room_id']
#     #     return RoomChatMessage.objects.filter(room_id=room_id).order_by('timestamp')

#     def get_queryset(self):
#         user = self.request.user
#         print('user----',user)
#         other_user_id = self.kwargs['other_user']
#         print('other user-----',other_user_id)
#         room = PrivateChatRoom.objects.filter(
#             (Q(user1=user) & Q(user2__id=other_user_id)) |
#             (Q(user2=user) & Q(user1__id=other_user_id))
#         ).first()
#         print('room-------',room)
#         if room:
#             return RoomChatMessage.objects.filter(room=room).order_by('timestamp')
#         return RoomChatMessage.objects.none()

class PrivateChatRoomListView(generics.ListAPIView):
    """
    API view to list all private chat rooms for the current user.
    """
    serializer_class = PrivateChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PrivateChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-messages__timestamp').distinct()
    

class RoomChatMessageListView(generics.ListAPIView):
    """
    API view to list all messages in a specific chat room.
    """
    serializer_class = RoomChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print('curr-----',user.id)
        other_user_id = self.kwargs['other_user']
        print('other-----',other_user_id)

        # Validate that other_user_id is an integer
        try:
            other_user_id = int(other_user_id)
        except ValueError:
            return RoomChatMessage.objects.none()

        # Find the chat room between the current user and the other user
        # room = PrivateChatRoom.objects.filter(
        #     (Q(user1=user) & Q(user2__id=other_user_id)) |
        #     (Q(user2=user) & Q(user1__id=other_user_id))
        # ).select_related('user1', 'user2').first()
        # print("****--room--",room)

        room = (PrivateChatRoom.objects.filter(user1=user, user2_id=other_user_id) |
            PrivateChatRoom.objects.filter(user1_id=other_user_id, user2=user)).first()
        print("****--room--",room)


        

        if room:
            messages = RoomChatMessage.objects.filter(room=room).select_related('user').order_by('timestamp')
            return messages
        return RoomChatMessage.objects.none()
