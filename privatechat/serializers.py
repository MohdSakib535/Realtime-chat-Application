from rest_framework import serializers
from privatechat.models import PrivateChatRoom,RoomChatMessage
from useraccount.models import CustomUser

class Friends_serializers(serializers.ModelSerializer):
    class Meta:
        model=PrivateChatRoom
        fields='__all__'




class UserSerializer(serializers.ModelSerializer):
    """Serializer to provide user details."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  # Add more fields if needed

class RoomChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""
    user = UserSerializer(read_only=True)  # Nested serializer for user details

    class Meta:
        model = RoomChatMessage
        fields = ['id', 'user', 'room', 'timestamp', 'content']
        # depth = 1  # Optionally, include related room data (e.g., room ID and details)


class PrivateChatRoomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChatRoom
        fields = ['id', 'user1', 'user2', 'is_active', 'last_message']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return RoomChatMessageSerializer(last_message).data
        return None