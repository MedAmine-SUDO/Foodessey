import logging
from datetime import datetime

from skpy import SkypeEditMessageEvent, SkypeEventLoop, SkypeNewMessageEvent

from env import password, username

current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"anyfood_{current_date}.log"

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SkypeListener(SkypeEventLoop):
    "Listen to a channel continuously"

    def __init__(self):
        token_file = ".tokens-app"
        super(SkypeListener, self).__init__(username, password, token_file)

    def onEvent(self, event):
        if isinstance(event, (SkypeNewMessageEvent, SkypeEditMessageEvent)):
            message = {
                "user_id": event.msg.userId,
                "chat_id": event.msg.chatId,
                "msg": event.msg.content,
            }
            if event.msg.chatId == "19:a6bd893165004176b7ca1103ac3460b8@thread.skype":
                if event.msg.content.startswith(
                    "@resto"
                ) or event.msg.content.startswith("@order"):
                    logging.info(message)


if __name__ == "__main__":
    skype_listener = SkypeListener()
    skype_listener.loop()
