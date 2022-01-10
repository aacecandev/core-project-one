import hydralit_components as hc
import streamlit as st
from hydralit import HydraApp

from app.accidents_app import AccidentsApp
from app.home_app import HomeApp
from app.user_app import UserApp

st.set_page_config(
    page_title="Core Project One",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="auto",
)

if __name__ == "__main__":

    over_theme = {"txc_inactive": "#FFFFFF"}
    app = HydraApp(
        title="Core Project One",
        favicon="🔥",
        hide_streamlit_markers=False,
        use_banner_images=[
            "./static/images/logo.png",
            None,
            {
                "header": "<h1 style='text-align:center;padding: 0px 0px;color:grey;font-size:200%;'>Core Project One</h1><br>"
            },
            None,
            "./static/images/logo.png",
        ],
        banner_spacing=[5, 30, 60, 30, 5],
        use_navbar=True,
        navbar_sticky=True,
        navbar_animation=True,
        navbar_theme=over_theme,
    )
    # Home button will be in the middle of the nav list now
    app.add_app("Home", icon="🏠", app=HomeApp(title="Home"), is_home=True)

    app.add_app("Accidents", icon="🚔", app=AccidentsApp(title="Accidents"))
    app.add_app("User Area", icon="👤", app=UserApp(title="User Area"))

    # run the whole lot
    app.run()
