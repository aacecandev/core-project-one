import json

import requests
import streamlit as st

###############
### FIND ALL ###
###############

# /accidents
def get_all():
    res = requests.get(st.secrets["url"] + "/accidents")
    return res.json()


def get_all_victims_grouped_by_month():
    res = requests.get(st.secrets["url"] + "/eda/victims-grouped-month")
    return res.json()


def get_all_victims_grouped_by_weekday():
    res = requests.get(st.secrets["url"] + "/eda/victims-grouped-weekday")
    return res.json()


def get_all_coordinates():
    res = requests.get(st.secrets["url"] + "/eda/coordinates")
    return res.json()


def get_all_vehicles_grouped_by_month():
    res = requests.get(st.secrets["url"] + "/eda/vehicles-grouped-month")
    return res.json()


def get_all_vehicles_grouped_by_weekday():
    res = requests.get(st.secrets["url"] + "/eda/vehicles-grouped-weekday")
    return res.json()


###############
### FIND ONE ###
###############

# /accidents/{id}
def find_accident(data):
    res = requests.get(st.secrets["url"] + "/accidents/" + data["id"]).json()
    return res


##############
### CREATE ###
##############

# /accidents/create
# requests.put(url, params={key: value}, args)
def create_accident(data):
    payload = {
        "victims": data["victims"],
        "vehicles_involved": data["vehicles"],
        "date": data["date"],
        "location": {
            "coordinates": [2.125624418258667, 41.34004592895508],
            "type": "Point",
        },
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    res = requests.put(
        st.secrets["url"] + "/accidents/create",
        data=json.dumps(payload),
        headers=headers,
    )
    return res


##############
### UPDATE ###
##############

# /accidents/update
# requests.patch(url, params={key: value}, args)
def update_accident(data):
    payload = {
        "id": data["id"],
        "victims": data["victims"],
        "vehicles_involved": data["vehicles"],
        "date": data["date"],
        "location": {
            "coordinates": [2.125624418258667, 41.34004592895508],
            "type": "Point",
        },
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    res = requests.patch(
        st.secrets["url"] + "/accidents/update",
        data=json.dumps(payload),
        headers=headers,
    )
    return res


##############
### DELETE ###
##############

# /accidents/delete
def delete_accident(data):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    res = requests.delete(st.secrets["url"] + "/accidents/delete/" + data["id"]).json()
    return res
