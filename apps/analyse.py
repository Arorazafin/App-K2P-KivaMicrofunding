import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
#from loremipsum import get_sentences

from app import app



# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead

layout = html.Div([
        html.Div(
            dcc.Tabs(
                children =[
                    dcc.Tab(label = 'Analyse dataset', value = 'tab-1', style = {'textAlign': 'left'}),
                    dcc.Tab(label = 'Analyse ML non-supervisé', value= 'tab-2',style = {'textAlign': 'left'}),
                    dcc.Tab(label = 'Analyse ML supervisé', value= 'tab-3',style = {'textAlign': 'left'}),
                    dcc.Tab(label = '...', value= 'tab-4'),
                ],
                colors={
                    "border": "white",
                    "primary": "green",
                    #"background": "lightgreen",
                },
                value='tab-1',
                id='tabs',
                vertical=True,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                   # 'textAlign': 'left',
                }
            ),
            style={'width': '20%', 'float': 'left'}
        ),
        html.Div(
            html.Div(id='tab-output'),
            style={'width': '80%', 'float': 'right'}
        )
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    data = [
        {
            'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
            'y': [219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                  350, 430, 474, 526, 488, 537, 500, 439],
            'name': 'Rest of world',
            'marker': {
                'color': 'rgb(55, 83, 109)'
            },
            'type': ['bar', 'scatter', 'box'][int(value[4:]) % 3]
        },
        {
            'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
            'y': [16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                  299, 340, 403, 549, 499],
            'name': 'China',
            'marker': {
                'color': 'rgb(26, 118, 255)'
            },
            'type': ['bar', 'scatter', 'box'][int(value[4:]) % 3]
        }
    ]

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'legend': {'x': 0, 'y': 1}
                }
            }
        ),
        html.Div('res')
    ])


# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)