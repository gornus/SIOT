############################
# Created on Sun Jan 12 23:06:09 2020
# author: Gordon Cheung
# CID: 01083012
# Project: 
############################
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from utils import *

def get_data():
    pd.set_option('mode.chained_assignment', None)
    
    HSI = get_gsheet("HSI")
    HKD = get_gsheet("HKD")
    WEATHER_HKO = get_gsheet("Weather")
    WEATHER_DS = get_gsheet("Weather2")
    
    # Cleaning out the duplicates and data arrays that are not useful to analysis
    HSI_cleaned = df_clean(HSI,['2. high', '3. low', '5. volume'])
    HKD_cleaned = df_clean(HKD, ['2. high', '3. low'])
    WHKO_cleaned = df_clean(WEATHER_HKO)
    WDS_cleaned = df_clean(WEATHER_DS)
    
    # adjusting the timestamp columns of all data
    form = '%Y-%m-%d %H:%M:%S'
    sheet_timestamp(HSI_cleaned, form)
    sheet_timestamp(HKD_cleaned, form)
    sheet_timestamp(WHKO_cleaned, form)
    sheet_timestamp(WDS_cleaned, form)
    
    # making sure the data are numbers
    HSI_cleaned = to_numeric(HSI_cleaned, ['1. open', '4. close'])
    HKD_cleaned = to_numeric(HKD_cleaned, ['1. open', '4. close'])
    WHKO_cleaned = to_numeric(WHKO_cleaned, ['temperature', 'humidity', 'rainfall', 'icon'])
    WDS_cleaned = to_numeric(WDS_cleaned, ['temperature', 'humidity', 'rainfall'])
    
    # open and close per minute data is still not that useful, the average is more representative:
    HSI_cleaned['value'] = (HSI_cleaned['1. open']+HSI_cleaned['4. close'])/2
    HSI_cleaned.drop(columns=['1. open', '4. close'], inplace=True)
    HKD_cleaned['value'] = (HKD_cleaned['1. open']+HKD_cleaned['4. close'])/2
    HKD_cleaned.drop(columns=['1. open', '4. close'], inplace=True)
    
    # when making financial decisions, the change in prices is often more important than the absolute value
    value_change(HSI_cleaned, 'value')
    value_change(HKD_cleaned, 'value')
    
    # mapping the weather icons for consistency
    WHKO_cleaned['icon'].replace(HKO_icons, inplace=True)
    WDS_cleaned['icon'].replace(DS_map, inplace=True)
    WHKO_cleaned.head()
    
    # standardising data
    data_standardising(HSI_cleaned, ['value'])
    data_standardising(HKD_cleaned, ['value'])
    data_standardising(WHKO_cleaned, ['temperature', 'humidity', 'rainfall'])
    data_standardising(WDS_cleaned, ['temperature', 'humidity', 'rainfall'])
    
    # find the lowest common starting point of the data
    base_time = max(min(HSI_cleaned['timestamp']),min(HKD_cleaned['timestamp']),min(WHKO_cleaned['timestamp']),min(WDS_cleaned['timestamp']))
    # map the timestamps according to this start to reduce the size of the numbers
    adjust_time(HSI_cleaned, base_time)
    adjust_time(HKD_cleaned, base_time)
    adjust_time(WHKO_cleaned, base_time)
    adjust_time(WDS_cleaned, base_time)
    
    # the financial data also has a higher sampled frequency and volitility, a moving average will help with analysis
    HSI_cleaned['moving_average'] = HSI_cleaned['value'].rolling(10,min_periods=1).mean()
    HKD_cleaned['moving_average'] = HKD_cleaned['value'].rolling(10,min_periods=1).mean()
    # merge the useful dataframes using the common timestamps
    merged = pd.merge(HSI_cleaned, WDS_cleaned[['timestamp', 'temperature', 'humidity', 'icon', 'temperature_std', 'humidity_std']], on="timestamp")
    data_standardising(merged, ['moving_average'])
    
    return merged

if __name__ == "__main__":
    get_data()