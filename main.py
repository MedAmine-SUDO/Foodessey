import os
import threading
from asyncio import new_event_loop, set_event_loop

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from flask import Flask, Response, request

from foodessey import FoodesseyBot

app = Flask(__name__)

APP_ID = os.environ.get("APP_ID")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

# Configure bot settings
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Create the bot instance
bot = FoodesseyBot()


@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    def call_bot_framework_adapter():
        loop = new_event_loop()
        set_event_loop(loop)
        loop.run_until_complete(
            adapter.process_activity(activity, auth_header, bot.on_turn)
        )
        loop.close()

    thread = threading.Thread(target=call_bot_framework_adapter)
    thread.start()
    thread.join()

    return Response(status=201)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
