from utils.common import *
from utils.requests import (
    get_all_vehicles_grouped_by_month,
    get_all_vehicles_grouped_by_weekday,
    get_all_victims_grouped_by_month,
    get_all_victims_grouped_by_weekday,
)


def victims_graph(query_time):
    if query_time == "Grouped by month":
        data = get_all_victims_grouped_by_month()
        columns = list(list(data)[0].keys())
        df = build_df(data, columns)
    elif query_time == "Grouped by weekday":
        data = get_all_victims_grouped_by_weekday()
        columns = list(list(data)[0].keys())
        df = build_df(data, columns)
    return df


def vehicles_graph(query_time):
    if query_time == "Grouped by month":
        data = get_all_vehicles_grouped_by_month()
        columns = list(list(data)[0].keys())
        df = build_df(data, columns)
    elif query_time == "Grouped by weekday":
        data = get_all_vehicles_grouped_by_weekday()
        columns = list(list(data)[0].keys())
        df = build_df(data, columns)
    return df
