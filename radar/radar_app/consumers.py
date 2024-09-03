import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'location_room'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        latitude = text_data_json['latitude']
        longitude = text_data_json['longitude']

        # Broadcast the coordinates to the group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'broadcast_coordinates',
                'latitude': latitude,
                'longitude': longitude
            }
        )

    async def broadcast_coordinates(self, event):
        latitude = event['latitude']
        longitude = event['longitude']

        # Send the coordinates to WebSocket clients
        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude
        }))
