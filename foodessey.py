import asyncio
from datetime import datetime, timedelta

from botbuilder.core import TurnContext
from botbuilder.schema import ActivityTypes, ChannelAccount


class FoodesseyBot:
    def __init__(self):
        self.restaurant_name = None
        self.orders = []
        self.order_deadline = None

    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            text = turn_context.activity.text.strip()
            sender_name = turn_context.activity.from_property.name
            sender_id = turn_context.activity.from_property.id

            if text.startswith("/lunch"):
                self.restaurant_name = text[len("/lunch") :].strip()
                self.orders = []
                self.order_deadline = datetime.now() + timedelta(minutes=1)
                self.initiator_id = sender_id

                response = (
                    f"Lunch orders are now open for {self.restaurant_name}. "
                    "Please submit your orders within the next 30 minutes."
                )
                await turn_context.send_activity(response)

                # Schedule a task to send a message after 30 minutes
                asyncio.get_running_loop().call_later(
                    1800,
                    asyncio.create_task,
                    self.send_order_deadline_message(turn_context),
                )

            elif text.startswith("/order") and self.restaurant_name is not None:
                now = datetime.now()
                if now <= self.order_deadline:
                    order = text[len("/order") :].strip()
                    if len(order) < 3:
                        await turn_context.send_activity(
                            "Invalid order. Please enter a valid order."
                        )
                    else:
                        self.orders.append((sender_name, order))
                        await turn_context.send_activity(
                            f"Order received from {sender_name}: {order}"
                        )
                else:
                    await turn_context.send_activity(
                        "Sorry, the order deadline has passed."
                    )
            else:
                await turn_context.send_activity(
                    "Invalid command. Use /lunch or /order."
                )

    async def send_order_deadline_message(self, turn_context: TurnContext):
        if self.restaurant_name is not None:
            await turn_context.send_activity(
                f"Orders for {self.restaurant_name} are now closed."
            )

            # Send the summary message to the initiator
            if self.initiator_id is not None:
                order_summary = "\n".join(
                    [f"{name}: {order}" for name, order in self.orders]
                )
                initiator_channel = ChannelAccount(id=self.initiator_id)
                summary_activity = turn_context.activity.create_reply(
                    f"Total orders for {self.restaurant_name}:\n{order_summary}"
                )
                summary_activity.recipient = initiator_channel
                await turn_context.adapter.create_conversation(
                    turn_context.activity, self.send_summary_message, summary_activity
                )

    async def send_summary_message(self, turn_context: TurnContext):
        await turn_context.send_activity(turn_context.activity.text)
