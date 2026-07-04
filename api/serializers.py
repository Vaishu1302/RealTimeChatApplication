from chat.models import GroupMessage
from rest_framework import serializers
from chat.models import Message, ChatGroup
from chat.models import GroupMessage
from rest_framework import serializers
from django.contrib.auth.models import User
from notification.models import Notification

from chat.models import (
    Message,
    ChatGroup,
    GroupMessage
)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatGroup
        fields = '__all__'


class GroupMessageSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = GroupMessage

        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email'
        ]
        
        


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
