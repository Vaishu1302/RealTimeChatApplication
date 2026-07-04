from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    message = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


# class ChatGroup(models.Model):

#     name = models.CharField(
#         max_length=100,
#         unique=True
#     )

#     members = models.ManyToManyField(
#         User
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     def __str__(self):
#         return self.name
class ChatGroup(models.Model):

    name = models.CharField(max_length=100)

    members = models.ManyToManyField(User)

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_groups',
        null=True,
        blank=True
    )

    group_photo = models.ImageField(
        upload_to='group_photos/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):

    group = models.ForeignKey(
        ChatGroup,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.message


class GroupFile(models.Model):

    group = models.ForeignKey(
        'ChatGroup',
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='group_files/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.file.name
