import json
import os
import zipfile
from typing import List

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_ercot_hourly_load_archive(url_json: str, years: List[int]) -> pd.DataFrame:
    """Parse ERCOR hourly load data from archives

    Data is downloaded from http://www.ercot.com/gridinfo/load/load_hist/ which only
    includes data up to the end of the previous month. For the most recent data, please
    use `parse_ercot_hourly_load_recent`

    Parameters
    ----------
    url_json : str
        Path to a local JSON file containing the URL of raw data load

    years : list of integer
        Years of which load data is parsed

    Returns
    -------
    Pandas.DataFrame
        Hourly load data as a Pandas DataFrame

    """
    with open(url_json, "r") as fr:
        urls = json.load(fr)

    if not os.path.exists("./tmp_data/"):
        os.mkdir("./tmp_data/")

    values = np.zeros((0, 9))
    index = pd.DatetimeIndex([])
    for year in years:
        print(year)
        url = urls[str(year)]  # type:str
        r = requests.get(url)
        local_path = os.path.join("./tmp_data/", url[url.rfind("/") + 1 :])
        with open(local_path, "wb") as fwb:
            fwb.write(r.content)

        if url.endswith(".zip"):
            excel_name = f"{year}.xlsx"
            zipfile.ZipFile(local_path).extractall("./tmp_data/")
            os.rename(
                os.path.join("./tmp_data/", zipfile.ZipFile(local_path).namelist()[0]),
                os.path.join("./tmp_data/", excel_name),
            )
            os.remove(local_path)
        elif url.endswith(".xls"):
            excel_name = f"{year}.xls"
            os.rename(local_path, os.path.join("./tmp_data/", excel_name))
        else:
            raise RuntimeError("The file is not zip or xls.")

        df = pd.read_excel(os.path.join("./tmp_data/", excel_name))
        df = df.set_index(df.columns[0])
        # deal with time stamp of 24:00:00
        if df.index.dtype == "O":
            df.index = pd.DatetimeIndex(
                [s[:11] + str(int(s[11:13]) - 1) + s[13:] for s in df.index]
            ) + pd.Timedelta("1H")
        df.index = df.index.round(freq="S")
        index = index.append(df.index)
        values = np.vstack([values, df.values])

    hourly_load = pd.DataFrame(
        values,
        index=index,
        columns=[
            "Coast",
            "East",
            "Far West",
            "North",
            "North Central",
            "South",
            "South Central",
            "West",
            "ERCOT",
        ],
    )
    hourly_load = hourly_load.sort_index()
    return hourly_load


def parse_ercot_hourly_load_recent(url_json: str) -> pd.DataFrame:
    """Parse ERCOR hourly load data for recent few weeks

    Data is downloaded from http://www.ercot.com/gridinfo/load which only includes data
    of the recent few weeks. Please use `parse_ercot_hourly_load_archive` for earlier
    data.

    Parameters
    ----------
    url_json : str
        Path to a local JSON file containing the URL of raw data load

    Returns
    -------
    Pandas.DataFrame
        Hourly load data as a Pandas DataFrame

    """
    with open(url_json, "r") as fr:
        urls = json.load(fr)
    url = urls["recent"]
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")
    if not os.path.exists("./tmp_data/"):
        os.mkdir("./tmp_data/")

    values = np.zeros((0, 9))
    index = pd.DatetimeIndex([])
    for counter, link in enumerate(soup.find_all("a")):
        if counter % 2:
            continue  # skip xml file
        r = requests.get("http://mis.ercot.com" + link["href"])
        local_path = os.path.join(
            "./tmp_data/", f"{link['href'][link['href'].rfind('=') + 1 :]}.zip"
        )
        with open(local_path, "wb") as fwb:
            fwb.write(r.content)
        zipfile.ZipFile(local_path).extractall("./tmp_data/")
        date = zipfile.ZipFile(local_path).namelist()[0][30:38]
        os.rename(
            os.path.join("./tmp_data/", zipfile.ZipFile(local_path).namelist()[0]),
            os.path.join("./tmp_data/", f"{date}.csv"),
        )
        os.remove(local_path)
        df = pd.read_csv(os.path.join("./tmp_data/", f"{date}.csv"))

        df.index = pd.DatetimeIndex(
            df["OperDay"]
            + " "
            + [str(int(time[:2]) - 1) + time[2:] for time in df["HourEnding"]]
        ) + pd.Timedelta("1H")

        df.index = df.index.round(freq="S")
        index = index.append(df.index)
        values = np.vstack([values, df.values[:, 2:11]])

    hourly_load = pd.DataFrame(
        values,
        index=index,
        columns=[
            "Coast",
            "East",
            "Far West",
            "North",
            "North Central",
            "South",
            "South Central",
            "West",
            "ERCOT",
        ],
    )
    hourly_load = hourly_load.sort_index()
    return hourly_load


if __name__ == "__main__":
    df = parse_ercot_hourly_load_archive(
        url_json="./ercot_hourly_load_urls.json",
        years=list(range(2005, 2022)),
    )
    df.to_csv("./tmp_data/archive.csv")

    df = parse_ercot_hourly_load_recent(url_json="./ercot_hourly_load_urls.json")
    df.to_csv("./tmp_data/recent.csv")
