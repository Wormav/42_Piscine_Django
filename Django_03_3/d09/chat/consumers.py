import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Appelé quand une connexion WebSocket est établie
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Vérifier si l'utilisateur est authentifié
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        # Rejoindre le groupe de la room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore

        await self.accept()

        # Envoyer un message de connexion à tous les membres du groupe
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
        Appelé quand une connexion WebSocket est fermée
        """
        if hasattr(self, "room_group_name") and not self.scope["user"].is_anonymous:
            # Envoyer un message de déconnexion
            username = self.scope["user"].username
            await self.channel_layer.group_send(  # type: ignore
                self.room_group_name,
                {
                    "type": "user_left",
                    "username": username,
                },
            )

            # Quitter le groupe de la room
            await self.channel_layer.group_discard(  # type: ignore
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Appelé quand un message est reçu du WebSocket
        """
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message = text_data_json["message"]
                username = self.scope["user"].username

                # Envoyer le message à tous les membres du groupe
                await self.channel_layer.group_send(  # type: ignore
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message,
                        "username": username,
                    },
                )
            except (json.JSONDecodeError, KeyError):
                # Ignorer les messages malformés
                pass

    async def chat_message(self, event):
        """
        Appelé quand un message de chat est reçu du groupe
        """
        message = event["message"]
        username = event["username"]

        # Envoyer le message au WebSocket
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
        Appelé quand un utilisateur rejoint le chat
        """
        username = event["username"]

        # Envoyer le message de connexion au WebSocket
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
        Appelé quand un utilisateur quitte le chat
        """
        username = event["username"]

        # Envoyer le message de déconnexion au WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_left",
                    "message": f"{username} has left the chat",
                    "username": username,
                }
            )
        )
