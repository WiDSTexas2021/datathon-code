import datetime
import os
import xml.etree.ElementTree as ET
from typing import List

import pandas as pd
import requests
from dotenv import load_dotenv

API_BASE_URL = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


def update_weather_history(csv: str, cities: List[str], years: List[int]) -> None:
    """Update weather history data of Texas cities.

    Weather history query uses API of worldweatheronline.com. It queries past weather
    of cities month by month following the list of years. Due to limit of API calls, a
    single call of the function may not obtained all data requested.

    Parameters
    ----------
    csv : str
        Local path of the CSV file that stores past weather data.
    cities : List[str]
        List of cities in Texas.
    years : List[int]
        List of years of data to query. The earliest available data is July 2008.

    """

    if os.path.exists(csv):
        df = pd.read_csv(csv)
    else:
        df = pd.DataFrame(
            columns=[
                "date",
                "time",
                "city",
                "tempC",
                "tempF",
                "windspeedMiles",
                "windspeedKmph",
                "winddirDegree",
                "winddir16Point",
                "weatherCode",
                "weatherDesc",
                "precipMM",
                "precipInches",
                "humidity",
                "visibility",
                "visibilityMiles",
                "pressure",
                "pressureInches",
                "cloudcover",
                "HeatIndexC",
                "HeatIndexF",
                "DewPointC",
                "DewPointF",
                "WindChillC",
                "WindChillF",
                "WindGustMiles",
                "WindGustKmph",
                "FeelsLikeC",
                "FeelsLikeF",
                "uvIndex",
            ]
        )
    for year in years:
        for month in range(12, 0, -1):
            if datetime.datetime.now() < datetime.datetime(year, month, 1):
                continue  # skip future month
            if datetime.datetime(year, month, 1) < datetime.datetime(2008, 7, 1):
                continue  # earliest date the API supports
            start_date_str = datetime.datetime(year, month, 1).strftime("%Y-%m-%d")
            if datetime.datetime.now() < datetime.datetime(
                year, month, 1
            ) + datetime.timedelta(30):
                end_date_str = datetime.datetime.now().strftime(
                    "%Y-%m-%d"
                )  # query up to today
            else:
                end_date_str = (
                    datetime.datetime(year, month, 1) + datetime.timedelta(30)
                ).strftime("%Y-%m-%d")
            for city in cities:
                print(f"{start_date_str} - {end_date_str} - {city}")
                if ((df["city"] == city) & (df["date"] == start_date_str)).any():
                    print("skip")
                    continue  # skip city/month queried before
                url = (
                    f"{API_BASE_URL}?key={API_KEY}"
                    f"&q={city.replace(' ', '+')},tx"
                    f"&date={start_date_str}&enddate={end_date_str}"
                )
                r = requests.get(url)
                if r.status_code == 200:
                    tree = ET.fromstring(r.content.decode())
                    for day in tree.findall("weather"):
                        for hour in day.findall("hourly"):
                            date = day.find("date")
                            if date is not None:
                                hour_data = {"date": date.text, "city": city}
                            else:
                                raise RuntimeError("No valid date is found.")
                            hour_data.update(
                                {
                                    key.tag: key.text
                                    for key in hour
                                    if key.tag != "weatherIconUrl"
                                }
                            )
                            df = df.append(hour_data, ignore_index=True)
                    df = df.sort_values(by=["date", "time", "city"])
                    df.to_csv(csv, index=False)
                else:
                    print(r.status_code)
                    print(r.content)


if __name__ == "__main__":
    cities = [
        "Houston",
        "Austin",
        "San Antonio",
        "Dallas",
        "Corpus Christi",
        "Brownsville",
        "Abilene",
        "Wichita Falls",
        "Midland",
        "Tyler",
    ]
    update_weather_history(
        csv="../../data/weather_history.csv",
        cities=cities,
        years=list(range(2021, 2007, -1)),
    )
