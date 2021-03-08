import json
import os
import re
from typing import Literal

import pandas as pd


def parse_texas_covid_19_data(
    url_json: str, data_type: Literal["confirmed", "deaths"]
) -> pd.DataFrame:
    """Parse Texas COVID-19 data by county from the JHU repository.

    Parameters
    ----------
    url_json : str
        Path to the JSON file including URLs to the data repository.
    data_type : "confirmed" or "deaths"
        Type of COVID-19 data to parse. "confirmed" for cumulative confirmed cases, or
        "deaths" for cumulative deaths count.

    Returns
    -------
    pd.DataFrame
        Parsed COVID-19 data for Texas per county.

    """
    with open(url_json, "r") as fr:
        url = json.load(fr)[data_type]
    df = pd.read_csv(url)
    df = (
        pd.DataFrame(
            df.loc[
                df["Province_State"] == "Texas",
                [
                    c
                    for c in df.columns
                    if (c == "Admin2") or (re.match("[0-9]*/[0-9]*/[0-9]*", c))
                ],
            ]
        )
        .set_index("Admin2")
        .T
    )
    df.index = df.index.rename("Date")
    df.index = pd.to_datetime(df.index)
    df.columns = df.columns.rename(None)

    if not os.path.exists("./tmp_data/"):
        os.mkdir("./tmp_data/")

    local_path = os.path.join("./tmp_data/", f"texas_covid_{data_type}.csv")
    df.to_csv(local_path)


if __name__ == "__main__":
    parse_texas_covid_19_data("covid_data_urls.json", "confirmed")
    parse_texas_covid_19_data("covid_data_urls.json", "deaths")
