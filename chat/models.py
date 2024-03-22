from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Chat(models.Model):
    sender = models.ForeignKey(
        UserModel, related_name="chat_sender", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        UserModel, related_name="chat_receiver", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat between {self.sender} and {self.receiver}"


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, related_name="chat_messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        UserModel, related_name="sender_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        UserModel, related_name="receiver_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    sent_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message between {self.sender} and {self.receiver}"
