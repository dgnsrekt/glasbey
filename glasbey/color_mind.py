import requests
import json
from random import choice

BASE_URL = "http://colormind.io/"
SUCESSFUL = 200

class ColorMind:

    @classmethod
    def get_palette(cls, model_name):
        current_models = cls.list_current_models()

        assert model_name in current_models, f"{model_name} isn't current. Use the following: {current_models}"

        return cls.palette_request(model_name)

    @classmethod
    def random_palette(cls):
        current_models = cls.list_current_models()

        model_name = choice(current_models)

        return cls.palette_request(model_name)

    @classmethod
    def palette_request(cls, model_name):
        base_palette = []

        data =  {"model": model_name}
        resp = requests.post(BASE_URL + "api/", data=json.dumps(data))
        assert resp.status_code == SUCESSFUL
        data = resp.json()

        for color in data["result"]:
            base_palette.append(tuple(color))

        return base_palette

    @classmethod
    def list_current_models(cls):
        resp = requests.get(BASE_URL + "list/")
        assert resp.status_code == SUCESSFUL
        data = resp.json()

        return data["result"]

def main():
    print(ColorMind.random_palette())
    print(ColorMind.get_palette("water_color"))
    print(ColorMind.get_palette("balls"))
    #{"result":[[154,17,20],[100,98,23],[94,102,40],[246,229,168],[26,67,35]]}


