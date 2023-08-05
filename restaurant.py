import Levenshtein

from mamachemi import MamaChemi


class RestaurantFactory:
    @staticmethod
    def create_restaurant(restaurant_name: str):
        correct_name = "Mama chemi"

        # Calculate the Levenshtein distance between the input name and the correct name
        distance = Levenshtein.distance(restaurant_name.lower(), correct_name.lower())

        # Set a threshold for similarity (adjust as needed)
        similarity_threshold = 3

        if distance <= similarity_threshold:
            return MamaChemi()
        else:
            return None
