import os
import pusher


pusher_client = pusher.Pusher(
    app_id=os.environ.get("PUSHER_APP_ID"),
    key=os.environ.get("PUSHER_KEY"),
    secret=os.environ.get("PUSHER_SECRET"),
    cluster=os.environ.get("PUSHER_CLUSTER"),
    ssl=True,
)


def send_ws_message(chat_id: str, message: str):
    return pusher_client.trigger(
        f"{chat_id}-chat", f"{chat_id}-message", {"message": message}
    )
