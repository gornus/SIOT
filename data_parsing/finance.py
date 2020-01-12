#!/usr/bin/python

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.foreignexchange import ForeignExchange
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import gspread, json, time

# parameters for getting data from the API
# Financial data from Alpha Vantage: https://www.alphavantage.co/
with open('api_keys.json') as json_file:
    keys = json.load(json_file)
api_key = keys["alpha_vantage"]
interval = 30 #number of minutes between each request, not requested every minute as there is a cap in requests and bulk data request is possible 
offset = timedelta(hours = 13) # convering the timezone of the data into local Hong Kong time

def finance_data():
    hsi_data = get_HSI_data()
    hkd_data = get_HKD_data()
    hsi_sheet, hkd_sheet = get_sheets()

    ## format the data retrieved from the API
    # insert the date column to the hsi data
    hsi_data.insert(0, "date", hsi_data.index.to_pydatetime()+offset)
    hsi_data["date"] = hsi_data["date"].astype(str)
    # insert the date column to the hkd data
    hkd_data.insert(0, "date", hkd_data.index.to_pydatetime()+offset)
    hkd_data["date"] = hkd_data["date"].astype(str)

    ## write to csv for local backup
    hsi_data.to_csv("HSI.csv", mode="a", header=False)
    hkd_data.to_csv("HKD.csv", mode="a", header=False)

    ## process the data into lists for publishing
    hsi_list = hsi_data.values.tolist()
    hkd_list = hkd_data.values.tolist()

    ## write to google sheet for cloud backup
    index = len(hsi_list)
    for i in range(index-interval-1, index-1):
        hsi_sheet.append_row(hsi_list[i])
        hkd_sheet.append_row(hkd_list[i])
        time.sleep(2) #pause to not exceed the limit set by Google


def get_HSI_data():
    ts = TimeSeries(key=api_key, output_format='pandas')
    hsi_data, meta_data = ts.get_intraday(symbol='^HSI',interval='1min', outputsize='compact')
    return hsi_data

def get_HKD_data():
    fx = ForeignExchange(key=api_key, output_format='pandas')
    hkd_data, meta_data = fx.get_currency_exchange_intraday('HKD', 'CNY', '1min', outputsize = 'compact')
    return hkd_data

def get_sheets():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    data_sheet = client.open("data")
    HSI_sheet = data_sheet.worksheet("HSI")
    HKD_sheet = data_sheet.worksheet("HKD")
    return HSI_sheet, HKD_sheet
