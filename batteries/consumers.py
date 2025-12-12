from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'dashboard'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Optionally handle messages from clients
        if text_data:
            await self.send(text_data=json.dumps({'echo': text_data}))

    async def dashboard.update(self, event):
        # Custom event to push JSON data to the client
        await self.send(text_data=json.dumps(event.get('data', {})))
