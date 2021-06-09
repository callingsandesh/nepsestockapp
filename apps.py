import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px

data = pd.read_csv("2010-05-09 to 2021-06-08.csv")

data=data[data['Sector']=='Commercial Banks']

data["Date"] = pd.to_datetime(data["Date"])
data.set_index('Date',inplace=True)
s_1=data[(data.index == '2021-06-08') | (data.index == '2020-07-08')]
s_1=s_1.sort_values('Closing Price')

price_change=s_1.reset_index()
price_change['Date']=price_change['Date'].astype(str)
price_change = price_change.pivot(index='Stock Symbol',columns='Date' ,values='Closing Price')
price_change['change']=round(((price_change['2021-06-08']-price_change['2020-07-08'] )/ price_change['2020-07-08']).mul(100),2)
price_change=price_change.sort_values('change')



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Percentage change over the range of time"


fig_1 = px.bar(s_1, x="Stock Symbol", y="Closing Price",
             color=s_1.index, barmode='group',title="Prices of stock of commercial banks of nepal over the specific period os time",
             height=400)

fig_2 = px.bar(price_change,
            x=price_change.index, y=price_change.change,
            text=price_change.change,
        )


app.layout = html.Div(children=[
    html.H1(children='Nepal Stock Exchange Analysis'),

    html.Div(children='''
        welcome
    '''),

    dcc.Graph(
        id='example1-graph',
        figure=fig_1
    ),
dcc.Graph(
        id='example2-graph',
        figure=fig_2
    )
])



if __name__ == "__main__":
    app.run_server(debug=True)