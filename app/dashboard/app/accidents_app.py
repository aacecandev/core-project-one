import time

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import streamlit as st
from hydralit import HydraHeadApp
from utils.common import *
from utils.geolocator import *
from utils.graphs import *
from utils.pdf_manager import create_pdf, email_manager
from utils.requests import get_all_coordinates


class AccidentsApp(HydraHeadApp):
    def __init__(self, title="Accidents", **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        # -------------------LOAD DATA ------------------------------------------

        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()

        for i in range(0, 101):
            status_text.text("%i%% Complete" % i)
            progress_bar.progress(i)
            time.sleep(0.02)
        status_text.text("Data Loaded!")
        progress_bar.empty()

        st.markdown(
            "<h2 style='text-align: center;'>Core Project One - EDA</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h2 style='text-align: center;'>You can use this tool to gain insights on how accidents occurs.</h2>",
            unsafe_allow_html=True,
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        # -------------------SIDEBAR ------------------------------------------

        st.sidebar.header("Accidents EDA")
        st.sidebar.subheader(
            "Use this tool to get a better understanding on how accidents occur in Barcelona city"
        )

        query_time = st.sidebar.selectbox(
            label="",
            options=["Grouped by month", "Grouped by weekday"],
            key="query_time",
        )
        query_radius = st.sidebar.radio(
            label="",
            options=["Line Chart", "Area Chart", "Bar Chart"],
            key="query_radius",
        )

        df_victims = victims_graph(query_time)
        df_vehicles = vehicles_graph(query_time)
        data_zipcodes = group_by_zipcode()

        uploaded_file = st.sidebar.file_uploader(
            "Upload a csv file",
            type=["csv"],
            help="Currently only 2018 is supported, please download the csv file from https://opendata-ajuntament.barcelona.cat/data/dataset/317e3743-fb79-4d2f-a128-5f12d2c9a55a/resource/6e2daeb5-e359-43ad-b0b5-7fdf438c8d6f/download/2018_accidents_vehicles_gu_bcn_.csv",
        )

        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)

        st.sidebar.subheader("You're currently viewing the accidents occured in 2017")

        create_pdf(df_victims)
        with open("streamlit.pdf", "rb") as pdf:
            st.sidebar.download_button(
                label="Download Report as PDF", data=pdf, mime="application/pdf"
            )

        email_address = st.sidebar.text_input(label="Enter your email address")
        if st.sidebar.button("Receive PDF by Email"):
            result = email_manager(email_address)
            if result == "Success!":
                st.sidebar.success("Email sent successfully!")
            else:
                st.sidebar.error("Email not sent!")

        # -------------------DATA ------------------------------------------

        with st.container():
            c1, c2 = st.columns(2)

            c1.header("Mean of victims ...")
            c2.header("Mean of vehicles involved ...")

            if query_radius == "Line Chart":
                c1.line_chart(df_victims)
                c2.line_chart(df_vehicles)
            elif query_radius == "Area Chart":
                c2.area_chart(df_vehicles)
                c1.area_chart(df_victims)
            elif query_radius == "Bar Chart":
                c2.bar_chart(df_vehicles)
                c1.bar_chart(df_victims)

        # -------------------------------

        st.header("Relation between victims and vehicles")

        frequency = df_victims
        exposition = df_vehicles

        palette = {
            "primary": "#c9893e",
            "secondary": "#F1F1F1",
            "background": "#404040",
            "text_color": "#7F7F7F",
        }

        fig, ax = plt.subplots(1, 1, figsize=(12, 2.5), dpi=100)

        if query_time == "Grouped by month":
            xlabels = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
        else:
            xlabels = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]

        ax = exposition["average"].plot(
            kind="bar",
            color=palette["primary"],
            label="Victims",
            width=0.35,
            zorder=3,
        )
        ax2 = ax.twinx()
        ax2.plot(
            frequency["average"].values,
            linestyle="solid",
            linewidth=0.5,
            color=palette["secondary"],
            zorder=2,
            marker="o",
        )

        fig.patch.set_facecolor(palette["background"])
        ax.set_facecolor(palette["background"])

        ax.spines["top"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["bottom"].set_linestyle("--")
        ax.spines["bottom"].set_linewidth(1)
        ax.spines["bottom"].set_color(palette["text_color"])
        ax2.spines = ax.spines

        ax.yaxis.set_visible(True)
        ax.xaxis.set_visible(True)
        ax.xaxis.set_ticks_position("top")
        ax.set_xticklabels(
            xlabels,
            color=palette["text_color"],
            weight="bold",
            rotation=45,
        )
        ax.xaxis.label.set_visible(False)
        ax.tick_params(axis="x", length=0)
        ax.grid(axis="y", color=palette["text_color"], linestyle="--", linewidth=1)
        ax2.xaxis = ax.xaxis

        ax.yaxis.set_visible(True)
        ax.yaxis.set_ticks_position("left")
        ax.set_yticklabels(ax.get_yticks(), color=palette["text_color"], weight="bold")
        ax.tick_params(axis="y", length=0)

        ax.set_ylim(0, 2)

        ax2.yaxis.set_visible(False)

        st.pyplot(fig)

        # -------------------------------

        st.header("Map of all accidents")

        st.slider("")

        with st.container():
            cordinates = get_all_coordinates()
            columns = list(list(cordinates)[0].keys())

            df = pd.DataFrame(cordinates, columns=columns)

            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/streets-v9",
                    initial_view_state={
                        "latitude": df["lat"].mean(),
                        "longitude": df["long"].mean(),
                        "zoom": 11,
                        "pitch": 50,
                    },
                    tooltip={
                        "html": "<b>Elevation Value:</b> {elevationValue}",
                        "style": {"backgroundColor": "steelblue", "color": "white"},
                    },
                    layers=[
                        pdk.Layer(
                            "HexagonLayer",
                            data=df,
                            get_position=["long", "lat"],
                            radius=50,
                            auto_highlight=True,
                            elevation_scale=4,
                            pickable=True,
                            elevation_range=[0, 1000],
                            extruded=True,
                        ),
                    ],
                )
            )

        # -------------------------------

        # st.header("Find out how many accidents there are in your area")

        # st.subheader("Select your area")

        # st.write(type(data_zipcodes))
