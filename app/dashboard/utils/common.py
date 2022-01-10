import pandas as pd


def build_df(data, columns):
    df = pd.DataFrame(data, columns=columns)
    df = df.set_index(list(columns)[1])
    return df
