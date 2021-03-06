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
icons = []
for i in range(len(raw_data['icon'].unique())):
    icons.append(raw_data[raw_data['icon']== raw_data['icon'].unique()[i]])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

siot_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

siot_app.layout = html.Div(children=[
    html.H1(children='Sensing and IOT'),
    ## Section 1: The outline part of the webpage
    html.Div(children=['Imperial College London Design Engineering Coursework by ',
                       html.A('Gordon Cheung', href='https://www.gordon-cheung.com/', target='_blank'), '.',
                       html.Br(), 'Full code repository can be found ',
                       html.A('here', href='https://github.com/gornus/SIOT', target='_blank'), '.'
                       ]),
    html.H2(children='Visualising the Data'),
    html.Div(children='This coursework focuses on relating the financial data and weather in Hong Kong.'),
    html.A('Click here to see the full dataset', 
             href='https://docs.google.com/spreadsheets/d/1tV4_d43dSW6wFto6RU1a4jnT_w-eLPLjLVA4uq3E_eo/edit?usp=sharing',
             target='_blank'),
    html.Div(children=['This section shows the data collected through the APIs, the list of APIs are as follows:',
                       html.Br(), 'Financial data through the Alpha Vantage API: ',
                       html.A('https://www.alphavantage.co/', href='https://www.alphavantage.co/', target='_blank'),
                       html.Br(), 'Weather data 1 through Hong Kong Observatory API: ',
                       html.A('https://www.hko.gov.hk/en/abouthko/opendata_intro.htm', href='https://www.hko.gov.hk/en/abouthko/opendata_intro.htm', target='_blank'),
                       html.Br(), 'Weather data 2 through Dark Sky API: ',
                       html.A('https://darksky.net/dev/docs', href='https://darksky.net/dev/docs', target='_blank'),
                       html.Br(),
                       'All data are collected live, refresh the page if you want to view the most recent data'
                       ]),
    ## Section 2: Viewing of the Data
    # options to select the set of data for viewing
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
    html.Br(),
    html.Div(id='data_display'),
    ## Section 3: showing the data analysis
    html.H2(children='Interacting with the Data'),
    html.Div(children=['Scatter plots of any combination of data columns']),
    html.Br(),
    html.Div([html.Label(['By Weather Icon',
                      dcc.RadioItems(
                        id='weather_icon',
                        options=[{'label': i, 'value': i} for i in ['Yes', 'No']],
                        value='Yes',
                        labelStyle={'display': 'inline-block'}
                        )])]),
    html.Div([
        html.Div([html.Label(['x axis:',
            dcc.Dropdown(
                id='x_column',
                options=[{'label': i, 'value': i} for i in columns],
                value='temperature_std'
            )]),
            dcc.RadioItems(
                id='x_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )],
            style={'width': '48%', 'display': 'inline-block'}),
        html.Div([html.Label(['y axis:',
            dcc.Dropdown(
                id='y_column',
                options=[{'label': i, 'value': i} for i in columns],
                value='change'
            )]),
            dcc.RadioItems(
                id='y_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),
    html.Div(id='data_interaction'),

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

# This second callback is dedicated for interacting with the data
@siot_app.callback(
    dash.dependencies.Output(component_id='data_interaction', component_property='children'),
    [dash.dependencies.Input('weather_icon', 'value'), 
     dash.dependencies.Input('x_column', 'value'),
     dash.dependencies.Input('x_type', 'value'),
     dash.dependencies.Input('y_column', 'value'),
     dash.dependencies.Input('y_type', 'value')]
)
def update_interaction(weather_icon, x_column, x_type, y_column, y_type):
    if weather_icon == "No":
        return[dcc.Graph(figure = dict(data = [dict(x = raw_data[x_column],
                                               y = raw_data[y_column],
                                               mode='markers',
                                               opacity = 0.8,
                                               marker = dict(size=10))],
                                    layout = dict(xaxis={'title': x_column,
                                                    'type': 'linear' if x_type == 'Linear' else 'log'
                                                },
                                                yaxis={'title': y_column,
                                                    'type': 'linear' if y_type == 'Linear' else 'log'
                                                },
                                                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                                                hovermode='closest'))
        )]
    else:
        data_dict=[]
        for i in icons:
            weather_dict = dict(x = i[x_column],
                                y = i[y_column],
                                name = i.iloc[0]['icon'],
                                mode = 'markers',
                                opacity = 0.8,
                                marker = dict(size=10))
            data_dict.append(weather_dict)
        return [dcc.Graph(figure = dict(data = data_dict,
                                    layout = dict(xaxis={'title': x_column,
                                                    'type': 'linear' if x_type == 'Linear' else 'log'
                                                },
                                                yaxis={'title': y_column,
                                                    'type': 'linear' if y_type == 'Linear' else 'log'
                                                },
                                                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                                                hovermode='closest'))
        )]

if __name__ == '__main__':
    siot_app.run_server(debug=True)