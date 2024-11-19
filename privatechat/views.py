from django.shortcuts import render
from  useraccount.models import CustomUser
from friends.models import FriendList,FriendRequest
from Notification.models import Notification
from django.shortcuts import get_object_or_404


def Private_chat(request):
    return render(request,'private_chats.html')