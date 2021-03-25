# Data

## ERCOT Hourly Power Load

- [`ercot_hourly_load.csv`](./ercot_hourly_load.csv) includes hourly power load in the eight ERCTO [weather zones](./ercotWeatherZoneMap.png). The most recent few weeks of data is from [ERCOT Actual System Load](http://mis.ercot.com/misapp/GetReports.do?reportTypeId=13101&reportTitle=Actual%20System%20Load%20by%20Weather%20Zone), while earlier data is from [ERCOT Load Data Archives](http://www.ercot.com/gridinfo/load/load_hist).

- [`weather_zone_cities.json`](./weather_zone_cities.json) lists all Texas cities in each ERCTO [weather zone](./ercotWeatherZoneMap.png).

- [`weather_zone_counties.json`](./weather_zone_counties.json) lists all Texas counties in each ERCTO [weather zone](./ercotWeatherZoneMap.png).

## COVID-19 Daily Data

- [`texas_covid_confirmed.csv`](./texas_covid_confirmed.csv) includes cumulative confirmed COVID-19 cases in Texas by county. The data is updated in [JHU COVID-19 data repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) in a daily basis.

- [`texas_covid_deaths.csv`](./texas_covid_confirmed.csv) includes cumulative COVID-19 deaths count in Texas by county. The data is updated in [JHU COVID-19 data repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) in a daily basis.

## Weather
- [`weather_history.csv`](./weather_history.csv) includes past weather data of 10 cities cross the 8 ECROT weather zones. The data is from [World Weather Online](https://www.worldweatheronline.com) and reported every 3 hours starting from July 1, 2008.
- [`weather_forecast.csv`](./weather_history.csv) includes weather forecast of 10 cities cross the 8 ECROT weather zones. The data is from [World Weather Online](https://www.worldweatheronline.com) and forecast every 3 hours in the next 13 days (including today).
