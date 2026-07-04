from django.contrib import admin

from .models import (
    Message,
    ChatGroup,
    GroupMessage
)

admin.site.register(Message)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
