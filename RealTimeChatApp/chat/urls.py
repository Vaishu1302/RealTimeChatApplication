from django.urls import path
from .import views
from .views import (
    user_list,
    private_chat,
    create_group,
    group_list,
    group_chat,

)
from .views import room
urlpatterns = [

    path(
        'users/',
        user_list,
        name='user_list'
    ),

    path(
        'chat/<int:user_id>/',
        private_chat,
        name='private_chat'
    ),
    path(
        'room/<str:room_name>/',
        room,
        name='room'
    ),
    path(
        'groups/',
        group_list,
        name='group_list'
    ),

    path(
        'create-group/',
        create_group,
        name='create_group'
    ),

    path(
        'group/<int:group_id>/',
        group_chat,
        name='group_chat'
    ),
    path(
        'group/remove-member/<int:group_id>/<int:user_id>/',
        views.remove_member,
        name='remove_member'
    ),
    path(
        'group/<int:group_id>/add-member/',
        views.add_member,
        name='add_member'
    ),
    path(
        'group/<int:group_id>/edit/',
        views.edit_group,
        name='edit_group'
    ),
    path(
        'group/<int:group_id>/delete/',
        views.delete_group,
        name='delete_group'
    ),
    path(
        'group-info/<int:group_id>/',
        views.group_info,
        name='group_info'
    ),
    path(
        'delete-message/<int:message_id>/',
        views.delete_message,
        name='delete_message'
    ),
    path(
        'group-file-delete/<int:file_id>/',
        views.delete_group_file,
        name='delete_group_file'
    ),
    path(
        'private-file/delete/<int:file_id>/',
        views.delete_private_file,
        name='delete_private_file'
    ),
]
