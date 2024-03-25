from django.urls import path
from .views import ChatAPIView, MessageListAPIView, SendMessageAPIView, redirect_user_to_chat


urlpatterns = [
    path("list/", ChatAPIView.as_view(), name="chats_list"),
    path(
        "messages/<int:chat_id>/list/",
        MessageListAPIView.as_view(),
        name="messages_list",
    ),
    path("messages/<int:chat_id>/send/", SendMessageAPIView.as_view(), name="send_message"),
    path("<int:user_id>/chat/", redirect_user_to_chat, name="user_chat"),
]
