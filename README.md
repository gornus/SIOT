# SIOT
 


This coursework focuses on relating the financial data and weather in Hong Kong.

APIs used:
* Financial data through the [Alpha Vantage API](https://www.alphavantage.co/)
* Weather data 1 through [Hong Kong Observatory API](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm)
* Weather data 2 through [Dark Sky API](https://darksky.net/dev/docs)

**Respective keys and credentials are not included in this repository.**

## Setup Overview

The data collection scripts are run on a Raspberry Pi to collect the live data for:
* Hang Seng Index Data
* Weather Data

All these data are then uploaded to Google Sheets through the [Google Sheets API](https://developers.google.com/sheets/api/) for data storage. The data analysis and web app then pulls the data from the same sheet for visualisation and analysis.

## Coursework 1: Sensing

To see the data collection in action, run data_parsing/main.py

New data will be append to the specified data sheet through user-specified credential keys.

## Coursework 2: IOT

data_analysis/data_anaysis.ipynb is the Jupyter notebook that contains all the data analysis and results.

data_analysis/main.py runs the web app that is based on the [Dash library](https://dash.plot.ly/)