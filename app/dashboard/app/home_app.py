import os

import streamlit as st
from hydralit import HydraHeadApp

MENU_LAYOUT = [1, 7]


class HomeApp(HydraHeadApp):
    def __init__(self, title="Home", **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        try:
            st.markdown(
                "<h2 style='text-align: center;'>This is the home page of <a href=https://github.com/aacecandev/core-project-one/>Core Project One</a> Data Explorer.</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h2 style='text-align: center;'>Feel free to reach me on <a href = https://www.linkedin.com/in/aacecan/>LinkedIn</a>.</h2>",
                unsafe_allow_html=True,
            )

            st.markdown("<br><br>", unsafe_allow_html=True)

            col_logo, col_text = st.columns(MENU_LAYOUT)

            col_logo.image(
                os.path.join(".", "static", "images", "data.png"),
                width=80,
            )

            col_text.subheader(
                "This project can be used to research about accidents occured in Barcelona city, Spain. It has been done using Jupyter-lab, FastAPI, Streamlit, MongoDB, Docker and a bunch more of interesting technologies. Visit the repo, PR are welcome!"
            )

            st.markdown("<br><br>", unsafe_allow_html=True)

            col_logo, col_text = st.columns(MENU_LAYOUT)
            col_logo.image(
                os.path.join(".", "static", "images", "classroom.png"),
                width=50,
            )
            col_text.info(
                "To start learning about Barcelona, go to the login page (dont't worry, i'll give you a test user 🤓)."
            )

        except Exception as e:
            st.image(
                os.path.join(".", "static", "iamges", "failure.png"),
                width=100,
            )
            st.error(
                "An error has occurred, someone will be punished for your inconvenience, we humbly request you try again."
            )
            st.error("Error details: {}".format(e))
