from rest_framework import serializers
from .models import Room
from django.contrib.auth import get_user_model
from useraccount.models import CustomUser


from rest_framework import serializers
from .models import Room
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RoomSerializer(serializers.ModelSerializer):
    created_by = serializers.EmailField()  # Accept email for created_by
    participants = serializers.ListField(
        child=serializers.EmailField(), required=False
    )  # Accept a list of emails for participants

    class Meta:
        model = Room
        fields = ['id', 'name', 'created_by', 'participants', 'is_video_enabled', 'created_at']
        read_only_fields = ['created_at']

    def validate_created_by(self, value):
        """Validate and convert email to a CustomUser instance."""
        try:
            return CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"User with email {value} does not exist.")

    def validate_participants(self, value):
        """Validate and convert emails to a list of CustomUser instances."""
        users = []
        for email in value:
            try:
                user = CustomUser.objects.get(email=email)
                users.append(user)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(f"User with email {email} does not exist.")
        return users

    def create(self, validated_data):
        """Override to handle participants."""
        created_by = validated_data.pop('created_by')
        participants = validated_data.pop('participants', [])
        room = Room.objects.create(created_by=created_by, **validated_data)
        room.participants.set(participants)
        return room

