import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is established
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Check if user is authenticated
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore

        await self.accept()

        # Send join message to all group members
        username = self.scope["user"].username
        await self.channel_layer.group_send(  # type: ignore
            self.room_group_name,
            {
                "type": "user_joined",
                "username": username,
            },
        )

    async def disconnect(self, code):
        """
        Called when a WebSocket connection is closed
        """
        if hasattr(self, "room_group_name") and not self.scope["user"].is_anonymous:
            # Send disconnect message
            username = self.scope["user"].username
            await self.channel_layer.group_send(  # type: ignore
                self.room_group_name,
                {
                    "type": "user_left",
                    "username": username,
                },
            )

            # Leave room group
            await self.channel_layer.group_discard(  # type: ignore
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Called when a message is received from WebSocket
        """
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message = text_data_json["message"]
                username = self.scope["user"].username

                # Send message to all group members
                await self.channel_layer.group_send(  # type: ignore
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message,
                        "username": username,
                    },
                )
            except (json.JSONDecodeError, KeyError):
                # Ignore malformed messages
                pass

    async def chat_message(self, event):
        """
        Called when a chat message is received from the group
        """
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": message,
                    "username": username,
                }
            )
        )

    async def user_joined(self, event):
        """
        Called when a user joins the chat
        """
        username = event["username"]

        # Send join message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_joined",
                    "message": f"{username} has joined the chat",
                    "username": username,
                }
            )
        )

    async def user_left(self, event):
        """
        Called when a user leaves the chat
        """
        username = event["username"]

        # Send leave message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_left",
                    "message": f"{username} has left the chat",
                    "username": username,
                }
            )
        )
