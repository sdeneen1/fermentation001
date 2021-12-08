import pandas as pd
import plotly.express as px
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_excel("SampleFermentation.xls")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['A', 'B'], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          df.Tank.unique()]),
    html.Div([
        html.Label(['Components Per Tank Options']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                    {'label':'5,7,22,24-tetraene-3B-ol', 'value': '5,7,22,24-tetraene-3B-ol'},
                    {'label':'7dehydro', 'value': '7dehydro'},
                    {'label':'Erg 5,7', 'value': 'Erg 5,7'},
                    {'label':'Erg', 'value': 'Erg'},
                    {'label':'M+2', 'value': 'M+2'},
                    {'label':'Zymo', 'value': 'Zymo'},
                    {'label':'Total Sterols', 'value': 'Total Sterols'},
                    {'label':'Total TG', 'value': 'Total TG'},
                    {'label':'OD', 'value': 'OD'},
                    {'label':'WCW', 'value': 'WCW'},
                    {'label':'DCW', 'value': 'DCW'},
                    {'label':'Feed mL', 'value': 'Feed mL'},
                    {'label':'Gly Res', 'value': 'Gly Res'},
                    {'label':'Glu Res', 'value': 'Glu Res'},
                    {'label':'NH4 Res', 'value': 'NH4 Res'},
                    {'label':'Base Weight', 'value': 'Base Weight'}
            ],
            value = 'Erg',
            multi = False,
            clearable=False,
            style={"width":"50%"}
        ),

    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToAdd': ['pan2d','select2d'],
                        },
                  className='six columns'
                  )
        ])
    ])
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my_dropdown', component_property='value'),
    Input(component_id='dpdn2', component_property='value')
)


def update_graph(my_dropdown, Tank_chosen):
    dff = df[df.Tank.isin(Tank_chosen)]
    linechart = px.line(
        data_frame = dff,
        x='Time',
        y = my_dropdown,
        color = 'Tank',
        labels={'Tank':'Tank', 'Time':'Time'},
        markers = True
        )
    linechart.update_layout(uirevision='foo')

    return linechart


@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    [Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value'),
    Input(component_id='my_dropdown', component_property='value')]
)
def update_side_graph(hov_data, clk_data, slct_data, Tank_chosen, my_dropdown):
    if hov_data is None:
        dff2 = df[df.Tank.isin(Tank_chosen)]
        dff2 = dff2[dff2.Time == 24]
        print(dff2)
        fig2 = px.pie(data_frame=dff2, values=my_dropdown, names='Tank',
                      title='Erg at 24h')
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = df[df.Tank.isin(Tank_chosen)]
        hov_Time = hov_data['points'][0]['x']
        dff2 = dff2[dff2.Time == hov_Time]
        fig2 = px.pie(data_frame=dff2, values=my_dropdown, names='Tank', title=f'{my_dropdown} at {hov_Time} hours')
        return fig2


if __name__ == '__main__':
    app.run_server(debug=False)