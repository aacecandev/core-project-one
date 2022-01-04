import requests

from ..config.api import url_base_api


def list_pokemon():
    return requests.get(url_base_api + "/pokemon").json()


def get_pokemon(name):
    query: dict = {"name": name}
    return requests.get(url=url_base_api + "/find/pokemon/", params=query).json()
