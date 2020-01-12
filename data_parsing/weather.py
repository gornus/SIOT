#!/usr/bin/python

import requests, csv, json, gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

## Powered by Dark Sky: https://darksky.net/poweredby/
with open('api_keys.json') as json_file:
    keys = json.load(json_file)
api_key = keys["dark_sky"]


def weather_data():
    weather_sheet = get_sheets("Weather")
    weather_sheet2 = get_sheets("Weather2")
    data = get_weather_data()
    data2 = get_weather_data2()
    write_csv('hk_weather.csv', data)
    write_csv('hk_weather2.csv', data2)
    weather_sheet.append_row(data)
    weather_sheet2.append_row(data2)

def get_weather_data():
    # initialising the data array
    data_list = []
    response = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?\
                            dataType=rhrread&lang=en")
    # time stamp
    time = response.json()["temperature"]["recordTime"]
    [day, time] = time.split("T")
    time = time.split("+")
    timestamp = day + " " + time[0]
    # Temperature
    temperature = response.json()["temperature"]["data"][1]['value']
    # Rainfall
    rainfall = response.json()["rainfall"]["data"][0]["max"]
    # Humidity
    humidity = response.json()["humidity"]["data"][0]["value"]
    # Weather icon, list of icons: https://www.hko.gov.hk/textonly/v2/explain/wxicon_e.htm
    icon = response.json()["icon"][0]
    
    row = [timestamp, temperature, humidity, rainfall, icon]
    return row

def get_weather_data2():

    # get the time in HK local time zone
    now = datetime.now()
    diff = timedelta(hours = 8)
    now = now + diff
    dt_string = now.strftime("%Y-%m-%dT%H:%M:00")
    
    ## Get the data from the Dark Sky API
    response = requests.get("https://api.darksky.net/forecast/"+api_key+
                            "/22.28552,114.15769,"+dt_string+"?exclude=minutely,hourly,daily,alerts,flags")
    # Reformat the time to match the other timestamps
    time = now.strftime("%Y-%m-%d %H:%M:00")
    # Temperature, Fahrenheit to Celcius
    temperature = round((response.json()["currently"]["temperature"]-32)/1.8,2)
    # Rainfall, inches to mm
    rainfall = round(response.json()["currently"]["precipIntensity"]*25.4, 2)
    # Humidity, decimal to percentage
    humidity = response.json()["currently"]["humidity"]*100
    # Weather icon
    icon = response.json()["currently"]["icon"]
    
    row = [time, temperature, humidity, rainfall, icon]
    return row


def get_sheets(name):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    data_sheet = client.open("data")
    weather_sheet = data_sheet.worksheet(name)
    return weather_sheet

def write_csv(name, data):
    with open(name, 'a') as c:
        writer = csv.writer(c)
        writer.writerow(data)
    c.close()
