############################
# Created on Sun Jan 12 16:18:10 2020
# author: Gordon Cheung
# CID: 01083012
# Project: SIOT
############################
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from sklearn import preprocessing
import gspread, json
import pandas as pd 
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf 
import numpy as np

with open('api_keys.json') as json_file:
    keys = json.load(json_file)
    
## Both weather APIs uses something known as "icon"
HKO_icons = {
    50: 'Sunny',
    51: 'Sunny Periods',
    52: 'Sunny Intervals',
    53: 'Sunny Periods with a Few Showers',
    54: 'Sunny Intervals with Showers',
    60: 'Cloudy',
    61: 'Overcast',
    62: 'Light Rain',
    63: 'Rain',
    64: 'Heavy Rain',
    65: 'Thunderstorms',
    70: 'Fine (Night)',
    71: 'Fine (Night)',
    72: 'Fine (Night)',
    73: 'Fine (Night)',
    74: 'Fine (Night)',
    75: 'Fine (Night)',
    76: 'Mainly Cloudy (Night)',
    77: 'Mainly Fine (Night)',
    80: 'Windy',
    81: 'Dry',
    82: 'Humid',
    83: 'Fog',
    84: 'Mist',
    85: 'Haze',
    90: 'Hot',
    91: 'Warm',
    92: 'Cool',
    93: 'Cold'
}
# Map these two different sets of icons together
DS_map = {
    'clear-day': 'Sunny',
    'clear-night': 'Mainly Fine (Night)',
    'rain': 'Rain',
    'snow': 'Snow',
    'sleet': 'Sleet',
    'wind': 'Windy',
    'fog': 'Fog',
    'cloudy': 'Overcast',
    'partly-cloudy-day': 'Cloudy',
    'partly-cloudy-night': 'Mainly Cloudy (Night)' 
}


################## Functions used for data processing ##################

def get_gsheet(RANGENAME):
    ### Retrieve sheet data using OAuth credentials and Google Python API.
    SPREADSHEET_ID = "1tV4_d43dSW6wFto6RU1a4jnT_w-eLPLjLVA4uq3E_eo"
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scopes)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGENAME).execute()
    df = gsheet2df(result)
    return df

def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df
    
def df_clean(df, names=None):
    # Get the dataframe, drop all the duplicates and specified columns (in a string array)
    df_cleaned = df.drop_duplicates()
    if names is not None: # drop columns if they are not useful
        df_cleaned.drop(columns=names, inplace=True)
    df_cleaned = df_cleaned.reset_index(drop=True)
    return df_cleaned

def sheet_timestamp(df, form):
    # parse the date string into datetime object using the specified format
    df['date'] = df['date'].apply(lambda x: 
                        datetime.strptime(x,form))
    df['timestamp'] = df['date'].apply(lambda x: datetime.timestamp(x)) #timestamp in the unix format
    df.sort_values(by=['timestamp'], inplace=True)
    df = df.reset_index(drop=True)
    return df

def to_numeric(df, names):
    # ensure the specified columns are numeric values for data plotting
    for name in names:
        df[name] = pd.to_numeric(df[name])
    return df

def standardising(data):
    #standardising the data array
    if (max(data)-min(data)) < 0.000001:
        return data
    else:
        scale = 1/(max(data)-min(data))
        data_scaled = scale*(data - min(data))
        return data_scaled

def data_standardising(df, names=None):
    if names is None:
        for key in df.keys():
            if df[key].dtype == 'int64' or df[key].dtype == 'float64':
                df[key+"_std"] = standardising(df[key])
    else:
        for name in names:
            if df[name].dtype == 'int64' or df[name].dtype == 'float64':
                df[name+"_std"] = standardising(df[name])
    return df

def adjust_time(df, base):
    df['timestamp'] = df['timestamp']-base
    df = df[df['timestamp']>=0]
    return df

def value_change(df, target):
    for i in range(len(df[target])):
        if i == 0:
            df.at[i, 'change'] = 0
#             print(df.iloc[i]['changed'])
        else:
            df.at[i, 'change'] = df.iloc[i]['value'] - df.iloc[i-1]['value']
    return df