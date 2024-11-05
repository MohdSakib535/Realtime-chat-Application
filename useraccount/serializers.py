from useraccount.models import CustomUser
from rest_framework import serializers


class user_account_Serializers(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'


