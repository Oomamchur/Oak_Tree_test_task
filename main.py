import json

import httpx

RESTAURANTS_API_URL = "https://uk.api.just-eat.io/restaurants/bypostcode/"


class JustEat:
    @staticmethod
    def get_restaurants_by_postcode(postcode: str):
        url = RESTAURANTS_API_URL + postcode

        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()

            restaurants = []
            rest_data = response.json()
            for rest in rest_data.get("Restaurants", []):
                """I would prefer to make a dictionary, but:
                Each array member should be its own associative array with the following properties
                """
                restaurant = [
                    rest.get("Name", "N/A"),
                    rest.get("RatingAverage", "N/A"),
                    [cuisine["Name"] for cuisine in rest.get("Cuisines", "N/A")],
                ]

                restaurants.append(restaurant)
            """IF there are restaurants at the specified postcode, we write data into .json file"""
            if len(restaurants) != 0:
                with open("data.json", "w") as data_json:
                    json.dump(restaurants, data_json)

            return restaurants

        except httpx.RequestError as e:
            return f"Network or request error: {e}"
        except httpx.HTTPStatusError as e:
            return f"HTTP error: {e}"


if __name__ == "__main__":
    postcode = "RH19"
    scrapper = JustEat()
    scrapper.get_restaurants_by_postcode(postcode)
