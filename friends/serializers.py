from friends.models import FriendList,FriendRequest
from rest_framework import serializers
from useraccount.serializers import user_account_Serializers




class friends_Serializer(serializers.ModelSerializer):
    friends=user_account_Serializers(many=True)
    class Meta:
        model=FriendList
        fields=['id','user','friends']


class friends_request_Serializer(serializers.ModelSerializer):
    # sender=user_account_Serializers()
    # receiver=user_account_Serializers()

    # or
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    def get_sender(self, obj):
        return obj.sender.username 

    def get_receiver(self, obj):
        return obj.receiver.username  


    class Meta:
        model=FriendRequest
        fields=['id','is_active','timestamp','sender','receiver']