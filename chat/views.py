from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, SendMessageSerializer
from .websocket import send_ws_message


class ChatAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(sender=user) | Q(receiver=user))


class MessageListAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer

    def get(self, request, chat_id, *args, **kwargs):
        user = request.user
        messages = Message.objects.filter(
            Q(chat_id=chat_id) & (Q(sender=user) | Q(receiver=user))
        ).order_by("created_at")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class SendMessageAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        chat = Chat.objects.filter(Q(sender=user) | Q(receiver=user))
        if not chat:
            chat = Chat.objects.create(sender=user, receiver_id=data.get("receiver"))
        else:
            chat = chat.last()

        message = Message.objects.create(
            chat=chat,
            sender=user,
            receiver_id=data.get("receiver"),
            content=data.get("content"),
            sent_at=timezone.now(),
        )

        send_ws_message(chat.id, message.content)
        message_serializer = MessageSerializer(message)
        return Response(message_serializer.data)
