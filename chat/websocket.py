import os
import pusher


pusher_client = pusher.Pusher(
    app_id=os.environ.get("PUSHER_APP_ID"),
    key=os.environ.get("PUSHER_KEY"),
    secret=os.environ.get("PUSHER_SECRET"),
    cluster=os.environ.get("PUSHER_CLUSTER"),
    ssl=True,
)


def send_ws_message(user_id: str, message: str):
    return pusher_client.trigger(
        "{user_id}-chat", f"{user_id}-message", {"message": message}
    )
