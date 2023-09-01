from rest_framework.serializers import ModelSerializer
from .models import Chat


class ChatDetailSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "created_at",
            "pk",
            "content",
        )
