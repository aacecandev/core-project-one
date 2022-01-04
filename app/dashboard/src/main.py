import math

import streamlit as st
from requests.api import get

from data.chart import radar_plot
from data.get import get_pokemon, list_pokemon

st.title("Core Project One")
st.text("A Data Science project to explore demographics of Barcelona city.")

# selection = st.selectbox("Select a dataset", ["Barcelona", "Madrid", "London"]) # mongo get collections
# st.text(selection)

all_pokemons = [poke["name"].title() for poke in list_pokemon()]
poke = st.multiselect("Select a Pokemon", all_pokemons)
poke_data = [get_pokemon(name.lower()) for name in poke]


## Columns

## number of pokemon selected
n = len(poke)
## number of rows
r = math.ceil(n / 5)

if n > 0:
    for i in range(r):
        image_columns = st.columns(n)
        for j in enumerate(5):
            # First syntax
            # image_columns[i].image(p["sprites"]['front_default'], width=100)
            if i * 5 + j < n:
                with image_columns[j]:
                    st.image(
                        poke_data[i * 5 + j]["sprites"]["front_default"], width=100
                    )


if n > 0:
    graph = base_chart()
    for p in poke_data:
        graph.add_trace(radar_plot(p["stats"], p["name"].title()))
    st.plotly_chart(graph)
