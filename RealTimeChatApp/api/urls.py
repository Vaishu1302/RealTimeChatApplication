from django.urls import path

from .views import (
    MessageListAPI,
    GroupListAPI,
    GroupMessageListAPI,
    MessageCreateAPI,
    GroupMessageCreateAPI,
    UserListAPI,
    NotificationListAPI,
    SecureMessageAPI
)

urlpatterns = [

    path(
        'messages/',
        MessageListAPI.as_view(),
        name='api_messages'
    ),

    path(
        'groups/',
        GroupListAPI.as_view(),
        name='api_groups'
    ),
    path(
        'group-messages/',
        GroupMessageListAPI.as_view(),
        name='group_messages_api'
    ),
    path(
        'send-message/',
        MessageCreateAPI.as_view(),
        name='send_message_api'
    ),
    path(
        'send-group-message/',
        GroupMessageCreateAPI.as_view(),
        name='send_group_message_api'
    ),
    path(
        'users/',
        UserListAPI.as_view(),
        name='users_api'
    ),

    path(
        'notifications/',
        NotificationListAPI.as_view(),
        name='notifications_api'
    ),
    path(
        'secure-messages/',
        SecureMessageAPI.as_view(),
        name='secure_messages'
    ),

]
