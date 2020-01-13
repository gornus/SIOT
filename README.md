# SIOT
 


This coursework focuses on relating the financial data and weather in Hong Kong.

APIs used:
* Financial data through the [Alpha Vantage API](https://www.alphavantage.co/)
* Weather data 1 through [Hong Kong Observatory API](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm)
* Weather data 2 through [Dark Sky API](https://darksky.net/dev/docs)

## Requirements

**Respective keys and credentials are not included in this repository.**

Credentials required to run this setup:
* [Google API credentials](https://developers.google.com/sheets/api/quickstart/python)
* [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)
* [Dark Sky API key](https://darksky.net/dev/register)

Libraries used that will require installation:
* [dash](https://dash.plot.ly/installation)
* [oauth2client](https://developers.google.com/sheets/api/quickstart/python)
* [gspread](https://developers.google.com/sheets/api/quickstart/python)
* [sklearn](https://scikit-learn.org/stable/install.html)
* [alpha_vantage](https://medium.com/alpha-vantage/get-started-with-alpha-vantage-data-619a70c7f33a)
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)

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