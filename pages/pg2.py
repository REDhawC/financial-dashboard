import dash
from dash import dcc, html, callback,dash_table, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd


dash.register_page(__name__, name='Financial Statements')

file_folder= "hksg"
file_folder1= file_folder+'/'
zcfzb=pd.read_csv(file_folder1+"zcfzb.csv",encoding='gb2312')
lrb=pd.read_csv(file_folder1+"lrb.csv",encoding='gb2312')
xjllb=pd.read_csv(file_folder1+"xjllb.csv",encoding='gb2312')
# page 2 data
df = px.data.tips()

zcfzb1=zcfzb.iloc[:,[0,1,2,3,4,5,6]]
lrb1=lrb.iloc[:,[0,1,2,3,4,5,6]]
xjllb1=xjllb.iloc[:,[0,1,2,3,4,5,6]]

dropdown_p2=dcc.Dropdown(['statement of financial position', 'cash flow statement', 'income statement']
                         , 'statement of financial position', id='page-2-dropdown')
table_p2=dash_table.DataTable(id='page-2-display-value',
data=[],
columns=[],
style_cell={'padding': '5px',
            'font_family':'microsoftyahei',
            'text_align': 'center'},
style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
page_size=150,
)



layout=dbc.Container([
    dbc.Row([
        dbc.Col([dropdown_p2], width=5)
    ], justify='left'),
    html.Br(),

    dbc.Row([
        dbc.Col([table_p2], width=12)
    ], justify='center'),
    html.Br(),
    dcc.Link('Go back to the top', href='/pg2'),
], fluid=True)

# Page 2 callbacks

@callback(
    Output('page-2-display-value', 'data'),
    Output('page-2-display-value', 'columns'),
              Input('page-2-dropdown', 'value'))
def display_value(user_input):
    if user_input == 'statement of financial position':
        data=zcfzb1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in zcfzb1.columns]
    elif user_input == 'cash flow statement':
        data=xjllb1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in xjllb1.columns]
    elif user_input == 'income statement':
        data=lrb1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in lrb1.columns]
    return data,columns

# layout = html.Div(
#     [
#         dbc.Row([
#             dbc.Col(
#                 [
#                     html.Img(src='assets/smoking2.jpg')
#                 ], width=4
#             ),
#             dbc.Col(
#                 [
#                     dcc.RadioItems(df.day.unique(), id='day-choice', value='Sat')
#                 ], width=6
#             )
#         ]),
#         dbc.Row([
#             dbc.Col(
#                 [
#                     dcc.Graph(id='bar-fig',
#                               figure=px.bar(df, x='smoker', y='total_bill'))
#                 ], width=12
#             )
#         ])
#     ]
# )
#
#
# @callback(
#     Output('bar-fig', 'figure'),
#     Input('day-choice', 'value')
# )
# def update_graph(value):
#     dff = df[df.day==value]
#     fig = px.bar(dff, x='smoker', y='total_bill')
#     return fig