import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = notebook

# 01:41:00
def radar_plot(stats, name):
    theta = [s["stats"]["name"].title() for s in stats]
    values = [s["base_stat"] for s in stats]
    radar = go.Figure(
        data=[go.Scatterpolar(r=values, theta=theta, fill="toself", name=name)]
    )
    return radar


def base_chart():
    return go.Figure()
