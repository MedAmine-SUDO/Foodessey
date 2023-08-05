import json
import re
from datetime import datetime

import Levenshtein
from skpy import Skype

from restaurant import RestaurantFactory

from env import password, username

skype = Skype(username, password)


class OrderParser:
    def __init__(self, logfile) -> None:
        self.logfile = logfile
        self.order_by_user = {}
        self.orderprice_by_user = {}
        self.resto = None
        self.menu = None

    def set_orders(self):
        with open(self.logfile, "r") as f:
            rows = f.readlines()
            for row in rows:
                match = re.search(r"{.*}", row)
                if match:
                    # Extract the JSON-like substring from the log line
                    json_str = match.group()
                    json_str_double_quotes = json_str.replace("'", '"')

                    # Convert the JSON string to a Python object (dictionary)
                    data_object = json.loads(json_str_double_quotes)
                    user_id, msg = (
                        data_object["user_id"],
                        data_object["msg"],
                    )

                    user = skype.contacts[user_id]

                    if msg.startswith("@resto"):
                        self.resto = msg[len("@resto") :].strip()
                        self.set_menu()
                        continue

                    order = msg[len("@order") :].strip()
                    order, supplements, special = self.validate_order(order)
                    if order:
                        self.order_by_user[str(user.name)] = {
                            "order": order,
                            "supp": supplements,
                            "special": special,
                        }

    def set_menu(self):
        restaurant = RestaurantFactory.create_restaurant(self.resto)
        self.menu = restaurant.get_menu()

    def validate_order(self, full_order):
        supp = None
        special = False
        full_order = full_order.lower()
        order_type = full_order.split()[0].strip()
        if order_type in self.menu.keys():
            order = full_order
            if "+" in full_order:
                order = full_order.split("+")[0].strip()
                supp = full_order.split("+")[1].strip()
            if "sp" in full_order:
                order = full_order.split("sp")[0].strip()
                special = True

            return self.correct_order(order), supp, special

        return None

    def correct_order(self, full_order):
        order_type = full_order.split()[0].strip()
        possible_orders = self.menu[order_type].keys()
        possible_orders_distance = {}
        for po in possible_orders:
            distance = Levenshtein.distance(po, full_order)
            possible_orders_distance[po] = distance
        correct_order = min(possible_orders_distance, key=possible_orders_distance.get)
        return correct_order

    def set_prices(self):
        for _, value in self.order_by_user.items():
            if value["special"]:
                value["supp"] = "oeuf + fromage"
            price = self.get_food_price(value)
            value["price"] = price

    def get_food_price(self, food_order):
        order = food_order["order"]
        supplements = None
        if food_order["supp"] is not None:
            supplements = [supp.strip() for supp in food_order["supp"].split("+")]

        categories = self.menu.keys()
        for category in categories:
            if isinstance(self.menu.get(category, {}), dict) and order in self.menu.get(
                category, {}
            ):
                price = self.menu[category][order]
                if supplements:
                    for supplement in supplements:
                        price += self.menu.get("supp", {}).get(supplement)
                return price
        return price


if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"anyfood_{current_date}.log"
    parser = OrderParser(log_filename)
    parser.set_orders()
    parser.set_prices()
    print(parser.order_by_user)
