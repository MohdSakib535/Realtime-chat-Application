from Notification.models import Notification
from rest_framework import serializers


class Notification_serializers(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields="__all__"