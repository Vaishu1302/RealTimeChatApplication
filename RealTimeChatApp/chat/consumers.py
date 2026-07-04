import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from .models import (
    ChatGroup,
    GroupMessage
)


class ChatConsumer(
    AsyncWebsocketConsumer
):

    async def connect(self):

        self.room_name = self.scope[
            'url_route'
        ]['kwargs']['room_name']

        self.room_group_name = (
            f'chat_{self.room_name}'
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(
        self,
        close_code
    ):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(
        self,
        text_data
    ):

        data = json.loads(
            text_data
        )

        user = self.scope["user"]

        # Typing Indicator

        if data.get('typing'):

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type': 'typing_message',
                    'user': user.username
                }

            )

        # Message

        elif data.get('message'):

            message = data['message']

            try:

                group = await sync_to_async(
                    ChatGroup.objects.get
                )(
                    id=self.room_name
                )

                await sync_to_async(
                    GroupMessage.objects.create
                )(
                    group=group,
                    sender=user,
                    message=message
                )

            except ChatGroup.DoesNotExist:

                pass

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username
                }

            )

    async def chat_message(
        self,
        event
    ):

        await self.send(

            text_data=json.dumps(

                {
                    'message': event['message'],
                    'user': event['user']
                }

            )

        )

    async def typing_message(
        self,
        event
    ):

        await self.send(

            text_data=json.dumps(

                {
                    'typing': True,
                    'user': event['user']
                }

            )

        )
