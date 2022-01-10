import os
from datetime import date, datetime

import streamlit as st
from hydralit import HydraHeadApp
from utils.geolocator import get_location
from utils.requests import (
    create_accident,
    delete_accident,
    find_accident,
    update_accident,
)


class UserApp(HydraHeadApp):
    def __init__(self, title="User Area", **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        try:
            st.markdown(
                "<h2 style='text-align: center;'>Welcome to your user area.</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h2 style='text-align: center;'>Here you can manage your data.</h2>",
                unsafe_allow_html=True,
            )
            st.markdown("<br><br>", unsafe_allow_html=True)

            with st.container():
                c1, c2 = st.columns(2)
                c1.subheader("Create a new accident")
                create_victims = c1.number_input(
                    key="create_victims",
                    label="Number of people involved",
                    step=1,
                    format="%i",
                    value=0,
                    min_value=0,
                    max_value=100,
                )
                create_vehicles = c1.number_input(
                    key="create_vehicles",
                    label="Number of vehicules involved",
                    step=1,
                    format="%i",
                    value=0,
                    min_value=0,
                    max_value=100,
                )
                create_date = c1.date_input(
                    key="create_date",
                    label="Date of the accident",
                    value=date.today(),
                    min_value=None,
                    max_value=None,
                )
                create_time = c1.time_input(
                    key="create_time",
                    label="Time of the accident",
                    value=datetime.min.time(),
                )
                create_location = c1.text_input(
                    key="create_location",
                    label="Where did the accident happen?",
                    max_chars=100,
                    type="default",
                )
                create_location_oid = c1.text_input(
                    key="create_location_oid",
                    label="The generated accident's ID",
                    max_chars=100,
                    type="default",
                )
                put = c1.button("Create accident")
                payload = {
                    "victims": create_victims,
                    "vehicles": create_vehicles,
                    "date": datetime.combine(create_date, create_time).isoformat(),
                    "location": {"type": "Point", "coordinates": [0.2, 0.3]},
                }
                if put:
                    res = create_accident(payload)
                    if res.status_code == 201:
                        c1.success("Accident created successfully")
                    else:
                        c1.error("Error creating accident")

                c2.subheader("Update an existing accident")
                update_victims = c2.number_input(
                    key="update_victims",
                    label="Number of people involved",
                    step=1,
                    format="%i",
                    value=0,
                    min_value=0,
                    max_value=100,
                )
                update_vehicles = c2.number_input(
                    key="update_vehicles",
                    label="Number of vehicules involved",
                    step=1,
                    format="%i",
                    value=0,
                    min_value=0,
                    max_value=100,
                )
                update_date = c2.date_input(
                    key="update_date",
                    label="Date of the accident",
                    value=date.today(),
                    min_value=None,
                    max_value=None,
                )
                update_time = c2.time_input(
                    key="update_time",
                    label="Time of the accident",
                    value=datetime.min.time(),
                )
                update_location = c2.text_input(
                    key="update_location",
                    label="Where did the accident happen?",
                    max_chars=100,
                    type="default",
                )
                update_location_oid = c2.text_input(
                    key="update",
                    label="The ID of the accident to update",
                    max_chars=100,
                    type="default",
                )
                patch = c2.button("update accident")
                payload = {
                    "id": update_location_oid,
                    "victims": update_victims,
                    "vehicles": update_vehicles,
                    "date": datetime.combine(update_date, update_time).isoformat(),
                    "location": {"type": "Point", "coordinates": [0.2, 0.3]},
                }
                if patch:
                    res = update_accident(payload)
                    if res.status_code == 201:
                        c2.success("Accident updated successfully")
                    else:
                        c2.error("Error creating accident")

                # c2.subheader("Delete an accident")

                # delete = c2.button("Delete accident")
                # if delete:
                #     c2.success("Accident deleted successfully!")
                # else:
                #     c2.error("An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.")

            with st.container():
                c3, c4 = st.columns(2)

                c3.subheader("Find an accident")

                find_oid = c3.text_input(
                    key="find",
                    value="",
                    label="Introduce an accident ID",
                    max_chars=100,
                    type="default",
                )
                find = c3.button("Find an accident")
                payload = {"id": find_oid}
                if find:
                    res = find_accident(payload)
                    if len(res.values()) <= 1:
                        c3.error("Accident not found")
                    else:
                        location = get_location(
                            res["location"]["coordinates"][1],
                            res["location"]["coordinates"][0],
                        )
                        c3.success("Accident found successfully")
                        c3.write("Victims: " + str(res["victims"]))
                        c3.write("Vehicles: " + str(res["vehicles_involved"]))
                        c3.write("Date: " + str(res["date"]))
                        c3.write("Location : " + str(location))

                c4.subheader("Delete an accident")

                delete_oid = c4.text_input(
                    key="delete",
                    value="",
                    label="Introduce an accident ID",
                    max_chars=100,
                    type="default",
                )

                delete = c4.button("Delete an accident")
                payload = {"id": delete_oid}
                if delete:
                    res = delete_accident(payload)
                    if res["message"] == "The accident has not been updated":
                        c4.error("Error deleting accident")
                    else:
                        c4.success("Accident deleted successfully")

        except Exception as e:
            st.image(
                os.path.join(".", "static", "images", "failure.png"),
                width=100,
            )
            st.error(
                "An error has occurred, someone will be punished for your inconvenience, we humbly request you try again."
            )
            st.error("Error details: {}".format(e))
