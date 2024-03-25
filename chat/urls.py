from django.urls import path
from .views import ChatAPIView, MessageListAPIView, SendMessageAPIView


urlpatterns = [
    path("list/", ChatAPIView.as_view(), name="chats_list"),
    path(
        "messages/<int:chat_id>/list/",
        MessageListAPIView.as_view(),
        name="messages_list",
    ),
    path("messages/<int:chat_id>/send/", SendMessageAPIView.as_view(), name="send_message"),
]
