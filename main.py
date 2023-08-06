from datetime import datetime
from order_parser import OrderParser
from env import password, username
from skpy import Skype

skype = Skype(username, password)
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"anyfood_{current_date}.log"


def format_data_as_string(data):
    result = f"Bill for {current_date}\n"
    for name, details in data.items():
        result += f"{name} => {details['price']}\n"
    return result


def send_message_to_groupchat(group_chat_id, message):
    chat = skype.chats[group_chat_id]
    chat.sendMsg(message)


if __name__ == "__main__":
    parser = OrderParser(log_filename)
    parser.set_orders()
    parser.set_prices()

    data = parser.order_by_user
    group_chat_id = parser.group_id

    formatted_data = format_data_as_string(data)
    send_message_to_groupchat(group_chat_id, formatted_data)
