import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Notification, Task, Interaction


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time notifications."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_add(
                f"user_{self.scope['user'].id}",
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                f"user_{self.scope['user'].id}",
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        pass

    async def notification_message(self, event):
        """Send notification to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message']
        }))


class DashboardConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time dashboard updates."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_add(
                "dashboard_updates",
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                "dashboard_updates",
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        pass

    async def dashboard_update(self, event):
        """Send dashboard update to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': event['data']
        }))
