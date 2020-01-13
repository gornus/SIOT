import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from get_data import get_data
from datetime import date, datetime

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


data = get_data()
days = data['date'].apply(lambda x: x.date()).unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

siot_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

siot_app.layout = html.Div(children=[
    html.H1(children='Sensing and IOT'),
    ## The outline part of the webpage
    html.Div(children=['Imperial College London Design Engineering Coursework by ',
                       html.A('Gordon Cheung', href='https://www.gordon-cheung.com/', target="_blank"), '.',
                       html.Br(), 'Full code repository can be found ',
                       html.A('here', href='https://github.com/gornus/SIOT', target="_blank"), '.'
                       ]),
    html.H2(children='Visualising the Data'),
    html.A('Click here to see the full dataset', 
             href='https://docs.google.com/spreadsheets/d/1tV4_d43dSW6wFto6RU1a4jnT_w-eLPLjLVA4uq3E_eo/edit?usp=sharing',
             target="_blank"),
    html.Div(children=['This section shows the data collected through the APIs, the list of APIs are as follows:',
                       html.Br(), 'Financial data through the Alpha Vantage API: ',
                       html.A('https://www.alphavantage.co/', href='https://www.alphavantage.co/', target="_blank"),
                       html.Br(), 'Weather data 1 through Hong Kong Observatory API: ',
                       html.A('https://www.hko.gov.hk/en/abouthko/opendata_intro.htm', href='https://www.hko.gov.hk/en/abouthko/opendata_intro.htm', target="_blank"),
                       html.Br(), 'Weather data 2 through Dark Sky API: ',
                       html.A('https://darksky.net/dev/docs', href='https://darksky.net/dev/docs', target="_blank")
                       ]),
    # drop down options to select the set of data for viewing
    html.H3(children='Processed dataset'),
    html.Label(["Start date:", 
                html.Div(dcc.Dropdown(id="start_date",
                                       options=[{'label': i,
                                                 'value': i
                                                 } for i in days],
                                        value=days[0]))]),
    html.Label(["End date:", 
                html.Div(dcc.Dropdown(id="end_date",
                                       options=[{'label': i,
                                                 'value': i
                                                 } for i in days],
                                        value=days[-1]))]),
    generate_table(data[['date','value','change','temperature','humidity','icon']]),
    html.Br(),
    html.H4(children='Plotting the basic data'),
    dcc.Graph(
        figure = dict(data = [dict(x = data['date'],
                                   y = data['value'],
                                   name = 'HSI data')],
                    layout = dict(title = 'Hang Seng Index Values',
                                  showlegend=True,
                                  legend=dict(x=0, y=1.0))
        
                    )
            )
        ]
    )

if __name__ == '__main__':
    siot_app.run_server(debug=True)