import json


class MamaChemi:
    def __init__(self):
        with open("mama_chemi.json", "r") as f:
            self.prices = json.load(f)

    def get_menu(self):
        return self.prices
