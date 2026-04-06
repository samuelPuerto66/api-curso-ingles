# usuarios/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

# usuarios/consumers.py

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Esta es la llave maestra: TODOS deben estar en este mismo grupo
        self.room_group_name = 'chat_general' 
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # El servidor repite el mensaje a la sala 'chat_general'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel_name': self.channel_name
            }
        )

    async def chat_message(self, event):
        # Este método se activa en el PC y en el Celular al mismo tiempo
        await self.send(text_data=json.dumps({
            'message': event['message'],
            # Si el canal que lo envía es el mismo que recibe, es 'mío'
            'is_me': self.channel_name == event['sender_channel_name']
        }))