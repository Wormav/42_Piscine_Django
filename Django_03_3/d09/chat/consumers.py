import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ChatRoom, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_room(self, room_name):
        """Get or create chatroom"""
        try:
            return ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, room, user, message_type, content):
        """Save message to database"""
        return Message.objects.create(
            room=room, user=user, message_type=message_type, content=content
        )

    @database_sync_to_async
    def get_last_messages(self, room):
        """Get the last 3 messages from the room with all needed data (Exercise 02)"""
        messages = (
            Message.objects.filter(room=room)
            .select_related("user")
            .order_by("-timestamp")[:3]
        )
        # Return in chronological order (oldest to newest) with all data
        result = []
        for message in reversed(messages):
            result.append(
                {
                    "content": message.content,
                    "username": message.user.username,  # type: ignore
                    "timestamp": message.timestamp.strftime("%H:%M:%S"),
                    "message_type": message.message_type,
                }
            )
        return result

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

        # Get the chatroom
        self.room = await self.get_room(self.room_name)
        if not self.room:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore

        await self.accept()

        # Send the last 3 messages when user connects (Exercise 02)
        last_messages = await self.get_last_messages(self.room)
        for message_data in last_messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "chat_message",
                        "message": message_data["content"],
                        "username": message_data["username"],
                        "timestamp": message_data["timestamp"],
                        "message_type": message_data["message_type"],
                    }
                )
            )

        # Save join message to database
        username = self.scope["user"].username
        await self.save_message(
            self.room,
            self.scope["user"],
            "user_joined",
            f"{username} has joined the chat",
        )

        # Send join message to all group members
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
        if (
            hasattr(self, "room_group_name")
            and not self.scope["user"].is_anonymous
            and hasattr(self, "room")
        ):
            # Save leave message to database
            username = self.scope["user"].username
            await self.save_message(
                self.room,
                self.scope["user"],
                "user_left",
                f"{username} has left the chat",
            )

            # Send disconnect message
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

                # Save message to database
                await self.save_message(
                    self.room, self.scope["user"], "message", message
                )

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
