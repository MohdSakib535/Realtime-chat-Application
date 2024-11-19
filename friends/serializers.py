from friends.models import FriendList,FriendRequest
from rest_framework import serializers
from useraccount.serializers import user_account_Serializers
from useraccount.models import CustomUser




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



class FriendsRequestSerializer(serializers.ModelSerializer):
    # sender = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    # receiver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'is_active']
        read_only_fields = ['id', 'is_active']

    def to_representation(self, instance):
    # Start with the default representation
        representation = super().to_representation(instance)
        
        # Add `from_user` details (both id and username)
        representation['sender'] = {
            'id': instance.sender.id,
            'username': instance.sender.username
        }

        # Add `to_user` details (both id and username)
        representation['receiver'] = {
            'id': instance.receiver.id,
            'username': instance.receiver.username
        }

        return representation