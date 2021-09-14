import json
import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AccessConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("NEW CONNECTION!")
        # self.room_name = self.scope['url_route']['kwargs']['room_code']
        # self.room_group_name = 'room_%s' % self.room_name
        #
        # # Join room group
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        await self.disconnect(1011)

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        version = response.get("version", None)
        r_time = response.get("time", None)
        card = response.get("card", None)

        if version:
            print("A v{} client just connected!".format(version))

        if r_time:
            print("{}: Got {}".format(datetime.datetime.now(), r_time))
            await self.send(text_data=str(r_time))

        if card:
            print("Got a card swipe! ({})".format(card))

    async def send_message(self, res):
        """Receive message from room group"""
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "payload": res,
                }
            )
        )
