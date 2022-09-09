import dash
from dash import dcc, html, callback,dash_table, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

file_folder= "hksg"
file_folder1= file_folder+'/'
ylnl=pd.read_csv(file_folder1+"ylnl.csv",encoding='gb2312')
chnl=pd.read_csv(file_folder1+"chnl.csv",encoding='gb2312')
cznl=pd.read_csv(file_folder1+"cznl.csv",encoding='gb2312')
yynl=pd.read_csv(file_folder1+"yynl.csv",encoding='gb2312')
chnl1=chnl.iloc[:,[0,1,2,3,4,5,6]]
ylnl1=ylnl.iloc[:,[0,1,2,3,4,5,6]]
cznl1=cznl.iloc[:,[0,1,2,3,4,5,6]]
yynl1=yynl.iloc[:,[0,1,2,3,4,5,6]]
cznl1=cznl1.dropna(axis=0)
dash.register_page(__name__, name='Financial Analysis')

df_p3=ylnl.transpose()
df_p3.columns = df_p3.iloc[0]
df_p3=df_p3.drop('报告日期',axis=0)
print(df_p3)


#page3
title_p3 = html.H2(children='',style={'color': 'black', 'fontSize':28})
slider_p3=dcc.Slider(0, 5,
        step=None,
        marks={
            1: 'Profitability',
            2: 'Repayment Capability',
            3: 'Growth Capability',
            4: 'Operating Capability',
        },value=1)
fig22=px.bar(px.bar(df_p3.iloc[0:10,0].astype(float)))
print(df_p3.iloc[0:10,0])
graph_p3=dcc.Graph(figure=fig22,id='sec')
slider2_p3=dcc.Slider(0, 5,
        step=None,
        marks={
            1: '应收账款周转率',
            2: '应收账款周转天数',
            3: '存货周转率',
            4: '固定资产周转率',
        },value=1)
table_p3=dash_table.DataTable(
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


layout= dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col([title_p3], width=9)
    ],justify='center'),

    dbc.Row([
        dbc.Col([slider_p3], width=10)
    ], justify='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([graph_p3], width=12)
    ], justify='center'),
    dbc.Row([
        dbc.Col([slider2_p3], width=12)
    ], justify='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([table_p3], width=12)
    ]),
    html.Br(),
    dcc.Link('Go back to the top', href='/pg3'),
], fluid=True)


# Page 3 callbacks1
@callback(
    Output(table_p3, 'data'),
    Output(table_p3, 'columns'),
    Output(title_p3, 'children'),
    Output(slider2_p3, 'marks'),
    Input(slider_p3, 'value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    marks = {
        1: 'Profitability Analysis',
        2: 'Repayment Capability Analysis',
        3: 'Growth Capability Analysis',
        4: 'Operating Capability Analysis',
    }
    if user_input == 1:
        data = ylnl1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in ylnl1.columns]
        marks1 = {
            1: 'Rate of Return on Total Assets',
            2: 'Main operation margins',
            3: 'Rate of Return on Total Assets',
            4: 'Ratio of Profits to Cost',
        }
    elif user_input == 2:
        data = chnl1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in chnl1.columns]
        marks1 = {
            1: 'Current Ratio',
            2: 'Quick Ratio',
            3: 'Cash Ratio',
            4: 'Interest Coverage Ratio',
        }
        print(df_p3)
    elif user_input == 3:
        data = cznl1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in cznl1.columns]
        marks1 = {
            1: 'Growth rate of main business revenue',
            2: 'Net asset growth rate',
            3: 'Growth rate of total assets',
        }

    elif user_input == 4:
        data = yynl1.to_dict('records')
        columns=[{'id': c, 'name': c} for c in yynl1.columns]
        marks1 = {
            1: 'Receivables Turnover Ratio',
            2: 'Days sales outstanding',
            3: 'Inventory Turnover',
            4: 'Total Assets Turnover',
        }
    return data,columns,marks[user_input],marks1


@callback(
    Output('sec', 'figure'),
    Input(slider_p3, 'value'),
    Input(slider2_p3, 'value')
)
def update_graph2(input1,input2):
    # function arguments come from the component property of the Input

    if input1 == 1 and input2 == 1:
        df_p3 = ylnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,0].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 ==1 and input2 == 2:
        df_p3 = ylnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,1].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 1 and input2 == 3:
        df_p3 = ylnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,2].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 1 and input2 == 4:
        df_p3 = ylnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,3].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    if input1 == 2 and input2 == 1:
        df_p3 = chnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,0].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 ==2 and input2 == 2:
        df_p3 = chnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,1].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 2 and input2 == 3:
        df_p3 = chnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,2].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 2 and input2 == 4:
        df_p3 = chnl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,3].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    if input1 == 3 and input2 == 1:
        df_p3 = cznl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,0].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 ==3 and input2 == 2:
        df_p3 = cznl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,2].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 3 and input2 == 3:
        df_p3 = cznl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,3].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    if input1 == 4 and input2 == 1:
        df_p3 = yynl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,0].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 ==4 and input2 == 2:
        df_p3 = yynl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,1].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 4 and input2 == 3:
        df_p3 = yynl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:5,2].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    elif input1 == 4 and input2 == 4:
        df_p3 = yynl.transpose()
        df_p3.columns = df_p3.iloc[0]
        df_p3 = df_p3.drop('报告日期', axis=0)
        fig=px.bar(df_p3.iloc[0:10,3].astype(float),text_auto=True,color_discrete_sequence= [px.colors.qualitative.Antique[3]])
    fig.update_layout({
        'font_family':'Arial',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig



#
# layout = html.Div(
#     [
#         dcc.Markdown('# This will be the content of Page 3 and much more!')
#     ]
# )