# coding=utf-8

import dash
import dash_auth
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np

USERNAME_PASSWORD_PAIRS = [
    ['lawrence','dash123'],
    ['marlon','dash123']
]

df = pd.read_excel(r'/home/marlon/dash_apps/app/data/Indicadores_CART_2012-2016.xlsx', sheet_name = 'BD',skiprows = 3, usecols=lambda x: 'Unnamed' not in x,)
#Substitute missing values with 0
df['Perspectiva'] = df['Perspectiva'].fillna(0000)
df['Tema'] = df['Tema'].fillna(0000)
df['Objetivo Estratégico'] = df['Objetivo Estratégico'].fillna(0000)
df['Indicador Proposto'] = df['Indicador Proposto'].fillna(0000)
#df = pd.read_csv(r'/home/marlon/dash_apps/app/data/Indicadores_CART_2012-2016.csv', skiprows = 3, usecols=lambda x: 'Unnamed' not in x,)

df1 = pd.read_excel(r'/home/marlon/dash_apps/app/data/Indicadores_CART_2012-2016.xlsx', sheet_name = 'BD',skiprows = 2, usecols=range(42,66))
df1.drop(df1.filter(regex="Unname"),axis=1, inplace=True)

df2 = pd.read_excel(r'/home/marlon/dash_apps/app/data/Indicadores_CART_2012-2016.xlsx', sheet_name = 'BD',skiprows = 3, usecols=range(42,66))
df2.drop(df2.filter(regex="Unname"),axis=1, inplace=True)

df3 = pd.read_excel(r'/home/marlon/dash_apps/app/data/Indicadores_CART_2012-2016.xlsx', sheet_name = 'BD',skiprows = 4, usecols=range(42,66))
df3.drop(df3.filter(regex="Unname"),axis=1, inplace=True)

df4 = pd.read_excel(r'/home/marlon/dash_apps/app/data/Indicadores_CART_2012-2016.xlsx', sheet_name = 'BD',skiprows = 5, usecols=range(42,66))
df4.drop(df4.filter(regex="Unname"),axis=1, inplace=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

#Construct year dataset (x values)
years = []
for i in df1[1:2]:
    years.append(i)

#Construct targets (realizado - meta) dataset
targets = []
for i in df2[1:2]:
#for i in df1.iloc[0,:]:
    targets.append(i)
#print(targets)

#Options are created as lists of dictionary with a label and a value
#Construct a dictionary of dropdown values for Perspectiva
options_perspectiva = []
for i in df['Perspectiva'].unique():
    options_perspectiva.append({'label':str(i),'value':i})

#Construct a dictionary of dropdown values for Tema
options_tema = []
for i in df['Tema'].unique():
    options_tema.append({'label':str(i),'value':i})

#Construct a dictionary of dropdown values for Objetivo estratégico
options_obj_estr = []
for i in df['Objetivo Estratégico'].unique():
    options_obj_estr.append({'label':str(i),'value':i})

#Construct a dictionary of dropdown values for Indicador proposto
options_indicador = []
for i in df['Indicador Proposto'].unique():
#    options_indicador.append(i)
    options_indicador.append({'label':str(i),'value':i})

app.layout = html.Div([
    html.Div([
#        html.Label('Perspectiva:'),
#        dcc.Dropdown(id = 'perspectiva', options = options_perspectiva)
#    ],style={'width': '50%', 'display': 'inline-block'}),
#    html.Div([
#        html.Label('Tema:'),
#        dcc.Dropdown(id = 'tema', options = options_tema)
#    ],style={'width': '50%', 'display': 'inline-block'}),
#    html.Div([
#        html.Label('Objetivo Estratégico:'),
#        dcc.Dropdown(id = 'obj_estr', options = options_obj_estr)
#    ],style={'width': '50%', 'display': 'inline-block'}),
#    html.Div([
        html.Label('Indicador Proposto:'),
        dcc.Dropdown(id = 'indicador', options = options_indicador, value = 'TIR (Projeto)')
    ]#,style={'width': '50%', 'display': 'inline-block'}
    ),
    dcc.Graph(id = 'graph')
], style={'padding':10})

@app.callback(
    Output('graph','figure'),
    [Input('indicador','value')]
)
def update_graph(indicador_selecionado):
    y2r = []
    y2m = []
    x = 0
    #indicador_selecionado = options_indicador[1]
    #print(indicador_selecionado)
    #print(options_indicador[1]['value'])
    #print(options_indicador[1])
    global id
    id = 0
    for idx in range(len(options_indicador)):
        #print(options_indicador[idx]['value'])
        if options_indicador[idx]['value'] == indicador_selecionado:
            print('index :',idx,' ',indicador_selecionado)
            id = idx

#    for i in df2.iloc[1,:]:
#    for i in df2.iloc[0,:]:
    print('opnieuw index :',id,' ',idx)
    for i in df2.iloc[id,:]:
        if x % 2 == 0:
            y2r.append(i)
        else:
            y2m.append(i)
        x = x + 1
    trace1 = go.Bar(
        x=years,  # NOC stands for National Olympic Committee
        y=y2m,
        name = 'meta',
        marker=dict(color='#FFD700') # set the marker color to gold
    )
    trace2 = go.Bar(
        x=years,
        y=y2r,
        name='realizado',
        marker=dict(color='#9EA0A1') # set the marker color to silver
    )
    traces = []
    traces.append(trace1)
    traces.append(trace2)
    return{
        'data': traces,
        'layout':go.Layout(
            xaxis={'title':'Mês'},
            yaxis={'title': indicador_selecionado}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
