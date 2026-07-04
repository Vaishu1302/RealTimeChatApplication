from chat.models import GroupMessage
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from notification.models import Notification
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView

from chat.models import Message
from chat.models import Message, ChatGroup

from .serializers import MessageSerializer

from chat.models import Message, ChatGroup
from .serializers import (
    MessageSerializer,
    GroupSerializer,
    GroupMessageSerializer,
    UserSerializer,
    NotificationSerializer
)


class MessageListAPI(ListAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class GroupListAPI(ListAPIView):

    queryset = ChatGroup.objects.all()
    serializer_class = GroupSerializer


class GroupMessageListAPI(ListAPIView):

    queryset = GroupMessage.objects.all()

    serializer_class = GroupMessageSerializer


class MessageCreateAPI(CreateAPIView):

    queryset = Message.objects.all()

    serializer_class = MessageSerializer


class GroupMessageCreateAPI(CreateAPIView):

    queryset = GroupMessage.objects.all()

    serializer_class = GroupMessageSerializer


class UserListAPI(ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer


class NotificationListAPI(ListAPIView):

    serializer_class = NotificationSerializer

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        )


class SecureMessageAPI(ListAPIView):

    queryset = Message.objects.all()

    serializer_class = MessageSerializer

    permission_classes = [
        IsAuthenticated
    ]
