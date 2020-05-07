# librerias
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#datos = pd.read_csv('srcdata/shot_dist_compiled_data_2019_20.csv')
datos = pd.read_csv('data.csv',delimiter=';')

app = dash.Dash(__name__)
server = app.server
dias = datos.dia.unique()
dias.sort()
app.layout = html.Div([
    html.Div([dcc.Dropdown(id='group-select', options=[{'label': i, 'value': i} for i in dias],
                           value='Todos', style={'width': '140px'})]),
    dcc.Graph('graph', config={'displayModeBar': False})])

@app.callback(
    Output('graph', 'figure'),
    [Input('group-select', 'value')]
)
def update_graph(valFiltro):
    import plotly.express as px
    return px.scatter(datos, x='dia', y='activos', size='nuevos')

if __name__ == '__main__':
    app.run_server(debug=False)
