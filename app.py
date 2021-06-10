import dash
from datetime import datetime as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
import my_theme

data = pd.read_csv("2010-05-09 to 2021-06-08.csv",parse_dates=['Date'],index_col='Date')

available_indicators = data['Sector'].dropna().unique()
print(available_indicators)


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



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1("PRICE CHANGES OF DIFFERENT SECTOR OVER RANGE OF DATE", style={'textAlign': 'center'}),
    html.Div(dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        calendar_orientation='horizontal',  # vertical or horizontal
        day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="Return",  # text that appears when no end date chosen
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=1,  # number of months shown when calendar is open
        min_date_allowed=dt(2010, 5, 10),  # minimum date allowed on the DatePickerRange component
        max_date_allowed=dt(2021, 6, 8),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=dt(2020, 7, 8),  # the month initially presented when the user opens the calendar
        start_date=dt(2020, 7, 8).date(),
        end_date=dt(2021, 6, 8).date(),
        display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        minimum_nights=2,  # minimum number of days between start and end date

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'

        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    )),
    html.Div(dcc.Dropdown(
                id='select-sector',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Commercial Banks'
            ),
            style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='mymap'),
    dcc.Graph(id="mymap2"),


])


@app.callback(
    [Output('mymap', 'figure'),Output('mymap2', 'figure')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('select-sector','value')]
)
def update_output(start_date, end_date,sector_name):
    print("date choosen",start_date,end_date)
    sector = data[data['Sector'] == sector_name]
    s_1 = sector[(sector.index == start_date) | (sector.index == end_date)]
    s_1 = s_1.sort_values('Closing Price')

    fig_1 = px.bar(s_1, x="Stock Symbol", y="Closing Price",
                   color=s_1.index, barmode='group',
                   title="Prices of stock of commercial banks of nepal over the specific period of time",

                 height=400)

    price_change = s_1.reset_index()
    price_change['Date'] = price_change['Date'].astype(str)
    price_change = price_change.pivot(index='Stock Symbol', columns='Date', values='Closing Price')
    price_change['change'] = round(((price_change[end_date] - price_change[start_date]) / price_change[start_date]).mul(100), 2)
    price_change=price_change.sort_values('change')
    fig_2 = px.bar(
            x=price_change.index, y=price_change.change,
            text=price_change.change,
            title="Percentage change of price over range of period"

        )

    return fig_1,fig_2


if __name__ == '__main__':
    app.run_server(debug=True)
