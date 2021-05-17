# WiDS Texas Datathon 2021 Data Repository

This data repository includes data for [WiDS Texas Datathon 2021](https://www.kaggle.com/c/wids-texas-datathon-2021). While the power load data and common related variables (e.g., weather, COVID-19) are public, we created an automated data pipeline to collect them in this repository for participants' convenience. The data is fetched from their original source into this repository once a day by some [GitHub Actions](../.github/workflows).

This data repository is NOT the minimal dataset that participants must use OR the maximal dataset that they could use. Participants should select the data based on their models. Participants are encouraged to use external public data if they believe it could improve their models.

To download the data to your local, please clone the git repository.

```bash
git clone git@github.com:WiDSTexas2021/datathon-code.git
cd datathon-code/data
```

To update your local data up to the state of the repository, please `git pull`.

## ERCOT Hourly Power Load

![ERCOT](https://github.com/WiDSTexas2021/hackathon/actions/workflows/update-ercot-hourly-load.yml/badge.svg)

- `ercot_hourly_load.csv` includes hourly power load in the eight ERCOT [weather zones](./ercotWeatherZoneMap.png). The most recent few weeks of data is from [ERCOT Actual System Load](http://mis.ercot.com/misapp/GetReports.do?reportTypeId=13101&reportTitle=Actual%20System%20Load%20by%20Weather%20Zone), while earlier data is from [ERCOT Load Data Archives](http://www.ercot.com/gridinfo/load/load_hist). Note that all timestamps include time zone information (UTC offset, which depends on daylight saving time).

- `weather_zone_cities.json` lists all Texas cities in each ERCOT [weather zone](./ercotWeatherZoneMap.png). This could help to align power load data with city-wise data (e.g. weather data).

- `weather_zone_counties.json` lists all Texas counties in each ERCOT [weather zone](./ercotWeatherZoneMap.png). This could help to align power load data with county-wise data (e.g. COVID-19 data).

## Weather

![Weather](https://github.com/WiDSTexas2021/hackathon/actions/workflows/update-weather.yml/badge.svg)

- `weather_history.csv` includes past weather data of 10 cities cross the 8 ECROT [weather zones](./ercotWeatherZoneMap.png). The data is from [World Weather Online](https://www.worldweatheronline.com) and reported every 3 hours starting from July 1, 2008. See [here](https://www.worldweatheronline.com/developer/api/docs/historical-weather-api.aspx#hourly) for details about each column.

- `weather_forecast.csv` includes weather forecast of 10 cities cross the 8 ECROT [weather zones](./ercotWeatherZoneMap.png). The data is from [World Weather Online](https://www.worldweatheronline.com) and forecast every 3 hours in the next 13 days (including today). See [here](https://www.worldweatheronline.com/developer/api/docs/local-city-town-weather-api.aspx#hourly) for details about each column.

## COVID-19 Daily Data

![COVID-19](https://github.com/WiDSTexas2021/hackathon/actions/workflows/update-covid.yml/badge.svg)

- `texas_covid_confirmed.csv` includes cumulative confirmed COVID-19 cases in Texas by county. The data is updated in [JHU COVID-19 data repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) in a daily basis.

- `texas_covid_deaths.csv` includes cumulative COVID-19 deaths count in Texas by county. The data is updated in [JHU COVID-19 data repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) in a daily basis.
