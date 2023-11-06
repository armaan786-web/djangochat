from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("Websocket Connected......")
        print("Channel Layer", self.channel_layer)
        print("Channel Name", self.channel_name)
        self.group_name = self.scope["url_route"]["kwargs"]["groupname"]
        print("group name........", self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive(self, text_data):
        print("Message receive from client", text_data)
        data = json.loads(text_data)
        print("Data...........", data)
        message = data["msg"]
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        print("Event.........", event)
        self.send(text_data=json.dumps({"msg": event["message"]}))

    def disconnect(self, close_code):
        print("Websocket Disconnected......", close_code)
