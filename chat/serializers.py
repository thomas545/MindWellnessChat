from rest_framework import serializers
from .models import Chat, Message
from users.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "sender",
            "receiver",
            "created_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "receiver",
            "content",
            "sent_at",
            "is_read",
            "created_at",
            "chat",
        )


class SendMessageSerializer(serializers.Serializer):
    receiver = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
