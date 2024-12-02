from rest_framework import serializers
from privatechat.models import PrivateChatRoom

class Friends_serializers(serializers.ModelSerializer):
    class Meta:
        model=PrivateChatRoom
        fields='__all__'