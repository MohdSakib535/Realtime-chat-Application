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
    # return render(request,'private_chats.html',context)
    return render(request,'privatechats2.html',context)



"""
APi section
"""

# from privatechat.serializers import Friends_serializers
# from privatechat.models import PrivateChatRoom
# class Friends_viewsets(viewsets.ModelViewSet):
#     queryset=PrivateChatRoom.objects.filter(Q(user1=request.user))

    
#     pass
