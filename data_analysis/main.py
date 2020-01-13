import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from get_data import get_data
from datetime import date, datetime

def generate_table(dataframe, max_rows):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


raw_data = get_data()
columns = raw_data.keys()
days = raw_data['date'].apply(lambda x: x.date()).unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

siot_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

siot_app.layout = html.Div(children=[
    html.H1(children='Sensing and IOT'),
    ## The outline part of the webpage
    html.Div(children=['Imperial College London Design Engineering Coursework by ',
                       html.A('Gordon Cheung', href='https://www.gordon-cheung.com/', target='_blank'), '.',
                       html.Br(), 'Full code repository can be found ',
                       html.A('here', href='https://github.com/gornus/SIOT', target='_blank'), '.'
                       ]),
    html.H2(children='Visualising the Data'),
    html.A('Click here to see the full dataset', 
             href='https://docs.google.com/spreadsheets/d/1tV4_d43dSW6wFto6RU1a4jnT_w-eLPLjLVA4uq3E_eo/edit?usp=sharing',
             target='_blank'),
    html.Div(children=['This section shows the data collected through the APIs, the list of APIs are as follows:',
                       html.Br(), 'Financial data through the Alpha Vantage API: ',
                       html.A('https://www.alphavantage.co/', href='https://www.alphavantage.co/', target='_blank'),
                       html.Br(), 'Weather data 1 through Hong Kong Observatory API: ',
                       html.A('https://www.hko.gov.hk/en/abouthko/opendata_intro.htm', href='https://www.hko.gov.hk/en/abouthko/opendata_intro.htm', target='_blank'),
                       html.Br(), 'Weather data 2 through Dark Sky API: ',
                       html.A('https://darksky.net/dev/docs', href='https://darksky.net/dev/docs', target='_blank')
                       ]),
    # drop down options to select the set of data for viewing
    html.H3(children='Viewing the processed dataset'),
    html.Label(['Start date:', 
                html.Div(dcc.Dropdown(id='start_date',
                                       options=[{'label': i,
                                                 'value': i
                                                 } for i in days],
                                        value=days[0]))]),
    html.Label(['End date:', 
                html.Div(dcc.Dropdown(id='end_date',
                                       options=[{'label': i,
                                                 'value': i
                                                 } for i in days],
                                        value=days[-1]))]),
    html.Br(),
    html.Label(['Number of data to show:', 
                html.Div(dcc.Slider(id='sample_amount',
                                    marks={i: '{}'.format(i) for i in range(1,21)},
                                    min=1,max=20,step=1,value=5))]),
    html.Label(['Columns to show:', 
                html.Div(dcc.Dropdown(id = 'columns',
                                      options=[{'label': i,
                                                 'value': i
                                                 } for i in columns],
                                    multi=True,
                                    value=['date','value','change','temperature','humidity','icon']))]),
    html.Div(id='data_display')
        ]
    )

## The callback elements on the web app
    
# This first callback is dedicated for displaying the data
@siot_app.callback(
    dash.dependencies.Output(component_id='data_display', component_property='children'),
    [dash.dependencies.Input('start_date', 'value'), 
     dash.dependencies.Input('end_date', 'value'),
     dash.dependencies.Input('sample_amount', 'value'),
     dash.dependencies.Input('columns', 'value')],
)
def update_graph(start_date, end_date, sample_amount, columns):
    filtered_df = raw_data[raw_data['date'].apply(lambda x: x.date())>= datetime.strptime(start_date,'%Y-%m-%d').date()]
    filtered_df = filtered_df[filtered_df['date'].apply(lambda x: x.date())<= datetime.strptime(end_date,'%Y-%m-%d').date()]
    return [generate_table(filtered_df[columns], sample_amount),
            dcc.Graph(figure = dict(data = [dict(x = filtered_df['date'],
                                               y = filtered_df['value'],
                                               name = 'HSI data')],
                        layout = dict(title = 'Hang Seng Index Values',
                                      showlegend=True))),
            dcc.Graph(figure = dict(data = [dict(x = filtered_df['date'],
                                               y = filtered_df['temperature'],
                                               name = 'Temperature data')],
                        layout = dict(title = 'Temperature Data',
                                      showlegend=True))),
            dcc.Graph(figure = dict(data = [dict(x = filtered_df['date'],
                                               y = filtered_df['humidity'],
                                               name = 'Humidity data')],
                        layout = dict(title = 'Humidity Data',
                                      showlegend=True)))]
    

if __name__ == '__main__':
    siot_app.run_server(debug=True)