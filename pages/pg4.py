import dash
from dash import dcc, html, callback,dash_table, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

file_folder= "hksg"
file_folder1= file_folder+'/'
cpsr=pd.read_csv(file_folder1+"cpsr.csv",encoding='gb2312')
hysr=pd.read_csv(file_folder1+"hysr.csv",encoding='gb2312')
cpsr['利润占比']=cpsr['利润占比'].str.strip('%').astype(float) / 100
hysr['利润占比']=hysr['利润占比'].str.strip('%').astype(float) / 100
cpsr=cpsr.dropna()
# chnl=chnl.iloc[:,[0,1,2,3,4,5,6]]
# ylnl=ylnl.iloc[:,[0,1,2,3,4,5,6]]
# cznl=cznl.iloc[:,[0,1,2,3,4,5,6]]
# yynl=yynl.iloc[:,[0,1,2,3,4,5,6]]
# cznl=cznl.dropna(axis=0)
dash.register_page(__name__, name='Revenue Sources Analysis')

#page4
title_p4 = html.H2(children='',style={'color': 'black', 'fontSize':30})
slider_p4=dcc.Slider(0, 3,
        step=None,
        marks={
            1: 'Products',
            2: 'Industries',
        },value=1)
graph_p4 = dcc.Graph(figure={})

layout= dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col([title_p4], width=6)
    ],justify='center'),

    dbc.Row([
        dbc.Col([slider_p4], width=6)
    ], justify='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([graph_p4], width=12)
    ]),
], fluid=True)


# Page 4 callbacks
@callback(
    Output(graph_p4, 'figure'),
    Output(title_p4, 'children'),
    Input(slider_p4, 'value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    marks = {
        1: 'Products Perspective',
        2: 'Industries Perspective',
    }
    if user_input == 1:
        fig = px.pie(cpsr
                     , names=cpsr.sort_values(by='利润占比', axis=0, ascending=False)['按产品']
                     , values=cpsr.sort_values(by='利润占比', axis=0, ascending=False)['利润占比']
                     ,hole=0.3
                     ,color_discrete_sequence=px.colors.sequential.Peach)
        fig.update_traces(textposition='inside', textinfo='label')
        fig.update_layout({
            'font_family': 'microsoftyahei',
            'font_size': 16,
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })


    elif user_input == 2:
        fig = px.pie(hysr
                     , names=hysr.sort_values(by='利润占比', axis=0, ascending=False)['按行业']
                     , values=hysr.sort_values(by='利润占比', axis=0, ascending=False)['利润占比']
                     ,hole=0.3
                     ,color_discrete_sequence=px.colors.sequential.Oryel)
        fig.update_traces(textposition='inside', textinfo='label')
        fig.update_layout({
            'font_family': 'microsoftyahei',
            'font_size': 16,
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })


    return fig,marks[user_input]


