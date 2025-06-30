import dash_core_components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    {"href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
     'rel': 'stylesheet',
     "Integrity": 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
     'crossorigin': 'anonymous'}, 1
]

i_df = pd.read_csv('IndividualDetails.csv')
total = i_df.shape[0]
active = i_df['current_status'].value_counts()[0]
recovered = i_df['current_status'].value_counts()[1]
deaths = i_df['current_status'].value_counts()[2]

options = [
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deaths','value':'Deaths'},
]

all = i_df['detected_state'].value_counts().reset_index()

active_cases = i_df[i_df['current_status']=='Hospitalized']
active_cases = active_cases.groupby('detected_state')['current_status'].value_counts().reset_index()
active_cases.drop(columns='current_status', inplace=True)

death_cases = i_df[i_df['current_status']=='Deceased']
death_cases = death_cases.groupby('detected_state')['current_status'].value_counts().reset_index()
death_cases.drop(columns='current_status', inplace=True)

recovered_cases = i_df[i_df['current_status']=='Recovered']
recovered_cases = recovered_cases.groupby('detected_state')['current_status'].value_counts().reset_index()
recovered_cases.drop(columns='current_status', inplace=True)

a_df = pd.read_csv('AgeGroupDetails.csv')

values = a_df['TotalCases'].values.tolist()
labels = a_df['AgeGroup'].values.tolist()

c_df = pd.read_csv('covid_19_india.csv')
temp_df = c_df[['Date','Confirmed']]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H1('COVID-19 Data Analysis', style={'color': '#000000', 'textAlign': 'center','fontSize': 60,'fontFamily': 'Segoe UI, Arial, sans-serif',
        'fontWeight': 'bold'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total Cases',className = 'text-light'),
                    html.H4(total,className = 'text-light'),
            ], className='card-body')
        ], className='card bg-warning'),
    ], className = 'col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Active Cases',className = 'text-light'),
                    html.H4(active,className = 'text-light'),
            ], className='card-body')
        ], className='card bg-info'),
    ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Recovered',className = 'text-light'),
                    html.H4(recovered,className = 'text-light'),
            ], className='card-body')
        ], className='card bg-success'),
    ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total Deaths',className = 'text-light'),
                    html.H4(deaths,className = 'text-light'),
            ], className='card-body')
        ], className='card bg-danger'),
        ], className='col-md-3'),
    ], className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Age Distribution',className = 'text-dark'),
                    dcc.Graph(figure=go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)],
                    layout=go.Layout(title='COVID-19 Cases per Age Group')
    )
)
                ],className = 'card-body'),
            ],className='card'),
        ],className = 'col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Cases per Day',className = 'text-dark'),
                    dcc.Graph(
                    figure=go.Figure(
                    data=[go.Scatter(x= temp_df['Date'], y = temp_df['Confirmed'], mode = 'lines')],
                    layout=go.Layout(xaxis_title='Date', yaxis_title='Confirmed', width=600, height=400)
    )
)
                ],className = 'card-body'),
            ],className='card'),
        ],className = 'col-md-6')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options = options,value = 'All'),
                    dcc.Graph(id='Bar')
                ],className = 'card-body'),
            ],className='card'),
        ],className='col-md-12')
    ], className='row')
], className='container')

@app.callback(Output('Bar', 'figure'),Input('picker','value'))
def plot_graph(input):
    if input == 'All':
        return {'data':[go.Bar(x= all['detected_state'], y=all['count'])],'layout':go.Layout(title='Total Cases')}
    elif input == 'Hospitalized':
        return {'data': [go.Bar(x=active_cases['detected_state'], y=active_cases['count'])], 'layout': go.Layout(title='Total Active Cases')}
    elif input == 'Deaths':
        return {'data': [go.Bar(x=death_cases['detected_state'], y=death_cases['count'])], 'layout': go.Layout(title='Total Deaths')}
    elif input == 'Recovered':
        return {'data': [go.Bar(x=recovered_cases['detected_state'], y=recovered_cases['count'])], 'layout': go.Layout(title='Total Recovered Cases')}

if __name__ == "__main__":
    app.run(debug=True)

