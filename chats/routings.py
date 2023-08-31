from django.urls import re_path
from .consumers import ChatConusmer

websocket_urlpattern = [
    re_path(
        r"^ws/chat/(?P<room_name>\w+)$",
        ChatConusmer.as_asgi(),
    )
]
