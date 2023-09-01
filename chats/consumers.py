from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Chat
from channels.layers import get_channel_layer
from .serializers import ChatDetailSerializer

# import json


class ChatConusmer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        chat_list = Chat.objects.all().order_by("-created_at")[0:10]
        serializer = ChatDetailSerializer(chat_list, many=True)
        self.send(serializer.data)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # http post의 db 갱신에 따른 내용만 허용할 것이기 때문에
    # websocket send 기능은 사용하지 않을 것

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name, {"type": "chat.message", "message": message}
    #     )

    # def send(self, event):
    #     message = event["message"]
    #     self.send(text_data=json.dumps(message))

    # anonymous chat implements
    @staticmethod
    @receiver(post_save, sender=Chat)
    def receive_instance(sender, instance, created, **kwargs):
        if created:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                channel_layer.room_group_name,
                ChatDetailSerializer(instance).data,
            )
