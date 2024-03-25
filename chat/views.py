from django.db.models import Q
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from rest_framework.renderers import (
    TemplateHTMLRenderer,
    JSONRenderer,
    BrowsableAPIRenderer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, SendMessageSerializer
from .websocket import send_ws_message


UserModel = get_user_model()


def home_page(request):
    # return render(request, "home.html")
    return redirect("chats_list")


class ChatAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChatSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer]
    template_name = "chats_list.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        users = UserModel.objects.exclude(Q(pk=user.pk) | Q(is_superuser=True))
        # chats = Chat.objects.filter(Q(sender=user) | Q(receiver=user))
        return Response({"users": users})


def redirect_user_to_chat(request, user_id):
    print("requ ->> ", request.user)
    print("uid ->>> ", user_id)

    chat = Chat.objects.filter(Q(sender_id=user_id) | Q(receiver_id=user_id))
    if not chat:
        chat = Chat.objects.create(sender=request.user, receiver_id=user_id)
    else:
        chat = chat.last()

    return redirect("send_message", chat_id=chat.id)


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
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer]
    template_name = "chat_details.html"

    def get(self, request, chat_id, *args, **kwargs):
        print("ccc ->> ", chat_id)
        user = request.user
        messages = Message.objects.filter(
            Q(chat_id=chat_id) & (Q(sender=user) | Q(receiver=user))
        ).order_by("created_at")
        chat = Chat.objects.get(id=chat_id)

        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "messages": messages,
                    "current_user": user,
                    "serializer": serializer,
                    "receiver_id": chat.receiver_id,
                    "chat_id": chat_id,
                }
            )

    def post(self, request, chat_id, *args, **kwargs):
        user = request.user
        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})

        data = serializer.validated_data

        chat = Chat.objects.get(id=chat_id)
        # chat = Chat.objects.filter(Q(sender=user) | Q(receiver=user))
        # if not chat:
        #     chat = Chat.objects.create(sender=user, receiver_id=data.get("receiver"))
        # else:
        #     chat = chat.last()

        message = Message.objects.create(
            chat=chat,
            sender=user,
            receiver_id=data.get("receiver"),
            content=data.get("content"),
            sent_at=timezone.now(),
        )

        send_ws_message(chat.id, message.content)
        return redirect("send_message", chat_id=chat_id)
