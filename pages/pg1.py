import dash
from dash import dcc, html, dash_table,callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import tushare as ts
import datetime as dt
import plotly.graph_objects as go


def getYesterday(weekday):
    today = dt.date.today()
    if weekday==0:
        oneday = dt.timedelta(days=3)
    elif weekday==6:
        oneday = dt.timedelta(days=2)
    else:
        oneday = dt.timedelta(days=1)
    yesterday = today - oneday
    yd = yesterday.strftime("%Y%m%d")
    return yd

def getpastdays(weekday):
    today = dt.date.today()
    if weekday==0:
        oneday = dt.timedelta(days=33)
    else:
        oneday = dt.timedelta(days=31)
    yesterday = today - oneday
    yd = yesterday.strftime("%Y%m%d")
    return yd
td = dt.datetime.today().strftime("%Y/%m/%d")
wd_t=dt.datetime.today().weekday()
td1 = td.replace('/', '')
currentYear = dt.datetime.now().year
firstday = str(currentYear) + '0101'

pro = ts.pro_api('17b3b989ac007724a18a682f9982aeacc42c1ec972c2349eb4ed5ab5')

# page 1 data




def get_pie_top10holders():
    df = pro.top10_holders(ts_code='000068.SZ', start_date=firstday, end_date=td1)
    print(df)
    fig = px.pie(df
                 , names=df.sort_values(by='hold_ratio', axis=0, ascending=False)['holder_name']
                 , values=df.sort_values(by='hold_ratio', axis=0, ascending=False)['hold_ratio']
                 ,hole=0.2
                 ,color_discrete_sequence=px.colors.sequential.Greens_r)
    fig.update_layout({
        'font_family':'microsoftyahei',
        'font_size':16,
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return html.Div([html.H4(children='Top 10 shareholders'),dcc.Graph(
        id='top10pie',
        figure=fig)])

def get_dailyprice():
    try:
        df= pro.daily(ts_code='000068.SZ', start_date=getYesterday(wd_t,td1), end_date=td1)
        df1=df.iloc[[0],[1,2,3,4,5,6]]
    except:
        df= pro.daily(ts_code='000068.SZ', start_date=firstday, end_date=td1)
        df1=df.iloc[[0],[1,2,3,4,5,6]]
    return dash_table.DataTable(
    data=df1.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df1.columns],
    page_size=10,style_cell={'textAlign': 'center','font_family':'microsoftyahei'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    )



def get_basic():
    df=pro.stock_company(ts_code='000068.SZ',exchange='SZSE')
    df1 = df.iloc[:, [2, 3, 4, 5, 6,7,8,9]]
    return html.Div([dash_table.DataTable(
    data=df1.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df1.columns],
    page_size=10,style_cell={'padding': '5px',
            'font_family':'microsoftyahei',
            'text_align': 'center'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        )


])

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])



dash.register_page(__name__, path='/', name='Company Profile') # '/' is home page

#page1





p1_graph = dcc.Graph(id='graph',figure={})
p1_checklist=dcc.Checklist(
    id='toggle-rangeslider',
    options=[{'label': 'Include Rangeslider',
              'value': 'slider'}],
    value=['slider'])
# Customize your own Layout
layout = dbc.Container([
    html.Br(),
    html.H4(children='Stock Price'),
    dbc.Row([
        dbc.Col([p1_graph], width=12)
    ], justify='left'),
    dbc.Row([
        dbc.Col([p1_checklist], width=6)
    ], justify='left'),
    get_dailyprice(),
    html.Br(),
  get_pie_top10holders(),
    html.Br(),
     get_basic(),
    html.Br(),

],fluid=True)


#Page 1 callbacks
@callback(
    Output(p1_graph, 'figure'),
    Input(p1_checklist, 'value')
)
def update_graph(value):
    df= pro.daily(ts_code='000068.SZ', start_date='20180101', end_date=td1)
    df=df.sort_values(by='trade_date',ascending=True)
    fig = go.Figure(go.Candlestick(
        x=df['trade_date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    ))
    # fig.update_layout(axis_rangeslider_visible='slider' in value),
    fig.update_xaxes(showgrid=False,dtick=40)
    fig.update_layout({
        'font_family':'microsoftyahei',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig




# layout = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         dcc.Dropdown(options=df.continent.unique(),
#                                      id='cont-choice')
#                     ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
#                 )
#             ]
#         ),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         dcc.Graph(id='line-fig',
#                                   figure=px.histogram(df, x='continent',
#                                                       y='lifeExp',
#                                                       histfunc='avg'))
#                     ], width=12
#                 )
#             ]
#         )
#     ]
# )
#
#
# @callback(
#     Output('line-fig', 'figure'),
#     Input('cont-choice', 'value')
# )
# def update_graph(value):
#     if value is None:
#         fig = px.histogram(df, x='continent', y='lifeExp', histfunc='avg')
#     else:
#         dff = df[df.continent==value]
#         fig = px.histogram(dff, x='country', y='lifeExp', histfunc='avg')
#     return fig
