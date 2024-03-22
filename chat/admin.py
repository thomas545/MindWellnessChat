from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "created_at",
        "modified_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "chat",
        "sender",
        "receiver",
        "sent_at",
        "is_read",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "sent_at",
        "is_read",
        "created_at",
        "modified_at",
    )
