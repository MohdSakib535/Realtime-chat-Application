from django.shortcuts import render
from rest_framework import routers ,viewsets
from friends.models import FriendList,FriendRequest
from friends.serializers import friends_Serializer,friends_request_Serializer
# Create your views here.

class Friend_List(viewsets.ModelViewSet):
    queryset = FriendList.objects.all()
    serializer_class = friends_Serializer


class Friend_request_List(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = friends_request_Serializer





