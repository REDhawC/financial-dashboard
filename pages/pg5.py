import dash
from dash import dcc, html, callback,dash_table, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import tushare as ts
import datetime as dt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNetCV,LinearRegression,Lasso
from sklearn import metrics
from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score


dash.register_page(__name__, name='Machine Learning Predictions')

td = dt.datetime.today().strftime("%Y/%m/%d")
wd_t=dt.datetime.today().weekday()
td1 = td.replace('/', '')
pro = ts.pro_api('17b3b989ac007724a18a682f9982aeacc42c1ec972c2349eb4ed5ab5')
df= pro.daily(ts_code='000068.SZ', start_date='20180101', end_date=td1)

df_y=df['close']
df_x=df['trade_date']
tm= dt.datetime.today()+dt.timedelta(days=1)

l1=[]
for i in range(30):
    d=dt.datetime.today()+dt.timedelta(days=i)
    d1= d.strftime("%Y/%m/%d")
    d2= d1.replace('/', '')
    l1.append(d2)
    print(d2)
dic1={'tradedate':l1}
print(dic1)
df_tm=pd.DataFrame(dic1)
#training
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size = 0.3)
x_tr1=np.array(x_train).reshape(-1, 1)
df_x1=np.sort(np.array(x_tr1).reshape(-1, 1),axis=0)
x_tr2=np.array(x_test).reshape(-1, 1)
df_x2=np.sort(np.array(x_tr2).reshape(-1, 1),axis=0)

model1 = LinearRegression()
model1.fit(df_x1, y_train)
predictions=model1.predict(df_x2)
mae1=metrics.mean_absolute_error(y_test, predictions)
mse1=metrics.mean_squared_error(y_test, predictions)
rmse1=np.sqrt(metrics.mean_squared_error(y_test, predictions))
pre1 = model1.predict(df_tm)

encv = ElasticNetCV(alphas=(0.1, 0.01, 0.005, 0.0025, 0.001), l1_ratio=(0.1, 0.25, 0.5, 0.75, 0.8))
encv.fit(df_x1 , y_train)
pre2 = encv.predict(df_tm)
predictions=encv.predict(df_x2)
mae2=metrics.mean_absolute_error(y_test, predictions)
mse2=metrics.mean_squared_error(y_test, predictions)
rmse2=np.sqrt(metrics.mean_squared_error(y_test, predictions))


lasso = Lasso(alpha=0.08, fit_intercept=True,
                          precompute=False,  copy_X=True, max_iter=1000,tol=1e-4, \
                          warm_start=False, positive=False, random_state=None,\
                          selection='cyclic')
lasso.fit(df_x1 , y_train)
pre3 = lasso.predict(df_tm)
predictions=lasso.predict(df_x2)
mae3=metrics.mean_absolute_error(y_test, predictions)
mse3=metrics.mean_squared_error(y_test, predictions)
rmse3=np.sqrt(metrics.mean_squared_error(y_test, predictions))

df_tm1=df_tm
df_tm1.insert(0, 'Lasso', pre3)
df_tm1.insert(0, 'ElasticNet', pre2)
df_tm1.insert(0, 'Linear Regression', pre1)

#page5
title_p5 = html.H2(children='',style={'color': 'black', 'fontSize':30})
select_p5= html.H4(children='Select your predicting method:',style={'color': 'dimgrey', 'fontSize':17})
slider_p5=dcc.Slider(0, 4,
        step=None,
        marks={
            1: 'Lasso',
            2: 'ElasticNet',
            3: 'Linear Regression',
        },value=1)
graph_p5= dcc.Graph(figure={})
title2_p5 = html.H2(children='',style={'color': 'grey', 'fontSize':12})
title3_p5 = html.H2(children='',style={'color': 'grey', 'fontSize':12})
title4_p5 = html.H2(children='',style={'color': 'grey', 'fontSize':12})
layout= dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col([select_p5], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([title_p5], width=6)
    ],justify='center'),

    dbc.Row([
        dbc.Col([slider_p5], width=6)
    ], justify='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([title2_p5], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([title3_p5], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([title4_p5], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_p5], width=12)
    ]),


], fluid=True)

# Page 5 callbacks
@callback(
    Output(graph_p5, 'figure'),
    Output(title_p5, 'children'),
    Output(title2_p5, 'children'),
    Output(title3_p5, 'children'),
    Output(title4_p5, 'children'),
    Input(slider_p5, 'value')
)
def update_graph(user_input):

    marks = {
        1: 'Lasso',
        2: 'ElasticNet',
        3: 'Linear Regression',
    }
    if user_input == 1:
        fig = px.line(df_tm1, x='tradedate', y=['ElasticNet', 'Linear Regression', 'Lasso'])
        fig.update_layout({
            'font_family': 'microsoftyahei',
            'font_size': 16,
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_traces(line=dict(width=3))
        words1 = 'Mean Absolute Error(MAE):' + str(mae1)
        words2='Mean Squared Error(MSE):' + str(mse1)
        words3='Root Mean Squared Error (RMSE):' + str(rmse1)

    elif user_input == 2:
        fig = px.line(df_tm1, x='tradedate', y=['ElasticNet', 'Linear Regression', 'Lasso'])
        fig.update_layout({
            'font_family': 'microsoftyahei',
            'font_size': 16,
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_traces(line=dict(width=3))
        words1 = 'Mean Absolute Error(MAE):' + str(mae2)
        words2='Mean Squared Error(MSE):' + str(mse2)
        words3='Root Mean Squared Error (RMSE):' + str(rmse2)

    elif user_input == 3:
        fig = px.line(df_tm1, x='tradedate', y=['ElasticNet', 'Linear Regression', 'Lasso'])
        fig.update_layout({
            'font_family': 'microsoftyahei',
            'font_size': 16,
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_traces(line=dict(width=3))
        words1 = 'Mean Absolute Error(MAE):' + str(mae3)
        words2='Mean Squared Error(MSE):' + str(mse3)
        words3='Root Mean Squared Error (RMSE):' + str(rmse3)
    return fig,marks[user_input],words1,words2,words3