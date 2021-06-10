import dash
from datetime import datetime as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go


raw_data=pd.read_csv("2010-05-09 to 2021-06-10.csv",parse_dates=['Date'])
data = raw_data.set_index('Date')

available_indicators = data['Sector'].dropna().unique()
available_symbol = data['Stock Symbol'].dropna().unique()
#print(available_indicators)


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2021, 5, 8),
        initial_visible_month=dt(2021, 6, 10),
        date=dt(2021, 6, 10)),
        style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    html.Div(
          html.Div(html.H3(" AS OF "+str(data.index[-1].strftime('%Y-%m-%d'))+"  ,3:00:00 PM", style={'textAlign': 'center'}))),
    html.H3("TOP GAINERS", style={'textAlign': 'center'}),
    dcc.Graph(id='table_gainers'),
    html.H3("TOP LOSERS", style={'textAlign': 'center'}),
    dcc.Graph(id='table_losers'),

    html.Div(dcc.Dropdown(
            id='stock_symbol',
            options=[{'label': i, 'value': i} for i in available_symbol],
            value='KBL'),
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    dcc.Graph(id='stock_price'),
    dcc.Graph(id='stock_returns'),
    dcc.Graph(id='stock_volatility')
                ,html.H1("PRICE CHANGES OF DIFFERENT SECTOR OVER RANGE OF DATE", style={'textAlign': 'center'}),
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
    ),style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    html.Div(dcc.Dropdown(
                id='select-sector',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Commercial Banks'
            ),
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    dcc.Graph(id='mymap'),
    dcc.Graph(id="mymap2"),



])


@app.callback(
    [Output('mymap', 'figure'),Output('mymap2', 'figure'),
     Output('stock_price','figure'),
     Output('stock_returns','figure'),
     Output('stock_volatility','figure'),
     Output('table_gainers','figure'),
     Output('table_losers','figure')
     ],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('select-sector','value'),
     Input('stock_symbol','value'),
     #Input('my-date-picker-single','date')
    ]
)
def update_output(start_date, end_date,sector_name,symbol):
    #print("date choosen",start_date,end_date)
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
    fig_2.update_layout(
        xaxis_title="Stock Symbol",
        yaxis_title="Percentage Change",

    )

    ##plotting price of specific stock
    s_2=raw_data[['Date','Stock Symbol','Closing Price']]
    s_2 = s_2.replace(0, np.NaN)
    s_2 = s_2.pivot_table(index='Date', columns='Stock Symbol', values='Closing Price')
    s_2 = s_2.interpolate(method='linear', limit_direction='forward', axis=0)
    symbol=symbol.upper()
    s_2=s_2[symbol].dropna()
    fig_3=px.line(x=s_2.index,y=s_2.values,title="Price chart of "+ str(symbol))
    fig_3.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",

    )

    returns=s_2.pct_change()
    fig_4 = px.line(x=returns.index, y=returns.values, title="% returns chart of " + str(symbol))
    fig_4.update_layout(
        xaxis_title="Date",
        yaxis_title="% returns",

    )

    volatility=returns.mul(returns.values)
    fig_5 = px.line(x=volatility.index, y=volatility.values, title="Volatity " + str(symbol))
    fig_5.update_layout(
        xaxis_title="Date",
        yaxis_title="% V",

    )
    today_date=data.index[-1]
    today = data.loc[today_date]
    today['percentage_change'] = (today['Closing Price'] - today['Previous Closing']).div(today['Previous Closing']).mul(100)
    top_gainers=today.sort_values('percentage_change',ascending=False)[:30]
    top_losers = today.sort_values('percentage_change',ascending=True)[:30]
    fig_6 = go.Figure(data=[go.Table(
        header=dict(values=list(['Traded Companies', 'Stock Symbol', 'No. Of Transaction', 'Max Price',
       'Min Price', 'Closing Price', 'Traded Shares', 'Amount',
       'Difference Rs.', 'Sector', 'percentage_change']),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[top_gainers['Traded Companies'], top_gainers['Stock Symbol'], top_gainers['No. Of Transaction'], top_gainers['Max Price'],
                           top_gainers['Min Price'],top_gainers['Closing Price'],top_gainers['Traded Shares'],top_gainers['Amount'],top_gainers['Difference Rs.'],
                           top_gainers['Sector'],top_gainers['percentage_change']],
                   fill_color='chartreuse',
                   align='left'))
    ])
    fig_7 = go.Figure(data=[go.Table(
        header=dict(values=list(['Traded Companies', 'Stock Symbol', 'No. Of Transaction', 'Max Price',
                                 'Min Price', 'Closing Price', 'Traded Shares', 'Amount',
                                 'Difference Rs.', 'Sector', 'percentage_change']),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(
            values=[top_losers['Traded Companies'], top_losers['Stock Symbol'], top_losers['No. Of Transaction'],
                    top_losers['Max Price'],
                    top_losers['Min Price'], top_losers['Closing Price'], top_losers['Traded Shares'],
                    top_losers['Amount'], top_losers['Difference Rs.'],
                    top_losers['Sector'], top_losers['percentage_change']],
            fill_color='crimson',
            align='left'))
    ])

    return fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7




server = app.server
app.title = "ANALYTICS !"

if __name__ == '__main__':
    app.run_server(debug=True)
