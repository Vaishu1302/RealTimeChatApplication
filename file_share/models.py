from django.db import models


from django.contrib.auth.models import User


class SharedFile(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files_sent'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files_received'
    )

    file = models.FileField(
        upload_to='chat_files/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.file.name
