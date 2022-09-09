import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, callback


import numpy as np
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc,dash_table,Input, Output
import plotly.express as px
import pandas as pd
import urllib
import urllib.request



def download_info():
    file_folder= "hksg"
    file_folder1= file_folder+'/'
    #资产负债表
    url_zc='http://quotes.money.163.com/service/zcfzb_000068.html?type=year'
    n1='zcfzb.csv'
    #利润表
    url_lr='http://quotes.money.163.com/service/lrb_000068.html?type=year'
    n2='lrb.csv'
    #现金流量表
    url_xj='http://quotes.money.163.com/service/xjllb_000068.html?type=year'
    n3='xjllb.csv'
    url_ylnl='http://quotes.money.163.com/service/zycwzb_000068.html?type=year&part=ylnl'
    n4='ylnl.csv'
    url_chnl='http://quotes.money.163.com/service/zycwzb_000068.html?type=year&part=chnl'
    n5='chnl.csv'
    url_cznl='http://quotes.money.163.com/service/zycwzb_000068.html?type=year&part=cznl'
    n6='cznl.csv'
    url_yynl='http://quotes.money.163.com/service/zycwzb_000068.html?type=year&part=yynl'
    n7='yynl.csv'
    url_cpsr='http://quotes.money.163.com/service/gszl_000068.html?type=cp'
    n8='cpsr.csv'
    url_hysr='http://quotes.money.163.com/service/gszl_000068.html?type=hy'
    n9='hysr.csv'
    url_dysr='http://quotes.money.163.com/service/gszl_000068.html?type=dy'
    n10='dysr.csv'



    l_u=[url_zc,url_lr,url_xj,url_ylnl,url_chnl,url_cznl,url_yynl, url_cpsr,url_hysr,url_dysr],
    l_n=[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10],
    dic1={n1:url_zc,n2:url_lr,n3:url_xj,n4:url_ylnl,n5:url_chnl,n6:url_cznl,n7:url_yynl,n8:url_cpsr,n9:url_hysr,n10:url_dysr}
    for i in dic1:
        path=file_folder1+str(i)
        urllib.request.urlretrieve(dic1[i],path)

#下载的时候再取消注释
# download_info()

file_folder= "hksg"
file_folder1= file_folder+'/'




app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            style=SIDEBAR_STYLE
)



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Financial Information Visualization Web App",className="header-title",
                         style={'font-weight': 'bold','fontSize':35, 'textAlign':'center','color':'saddlebrown'}))
    ]),
    dbc.Row([
        dbc.Col(html.Div("creator:HAO CHEN",className="header-title",
                         style={'font-weight': 'bold','fontSize':17, 'textAlign':'center','color':'chocolate'}))
    ]),
    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col (
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)
