import geopy
from geopy.geocoders import Nominatim
from utils.requests import get_all

geolocator = Nominatim(user_agent="name-of-your-user-agent")


def group_by_zipcode():
    data = get_all()
    return data


def get_location(latitude, longitude):
    location = geolocator.reverse(f"{latitude}, {longitude}")
    return location.address
