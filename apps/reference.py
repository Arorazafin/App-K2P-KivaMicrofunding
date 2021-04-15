import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
        html.Div(
            dcc.Tabs(
                children =[
#                    dcc.Tab(label = 'Methodologie', value = 'tab-1'),
                    dcc.Tab(label = 'Réference', value= 'tab-1'),
#                    dcc.Tab(label = 'Definition 2', value= 'tab-3'),
                    dcc.Tab(label = '...', value= 'tab-2'),
                ],
                colors={
                    "border": "white",
                    "primary": "green",
                    #"background": "lightgreen",
                },
                value='tab-1',
                id='tabs-faq',
                vertical=True,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                    'textAlign': 'left',
                }
            ),
            style={'width': '20%', 'float': 'left'}
        ),
        html.Div(
            html.Div(id='tab-output-faq'),
            style={'width': '80%', 'float': 'right'}
        )
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })



@app.callback(
    Output('tab-output-faq', 'children'),
    [Input('tabs-faq', 'value')])
def display_content(value):
    if value == 'tab-1':
        # chld = html.Div(
        #         id="content-methodo",
        #         children=[
        #             #html.H4("Méthodologie"),
        #             dcc.Markdown('''
        #                     # Objectif:  

        #             ''')  
        #         ]
        # )

    #elif value == 'tab-2':
        chld = html.Div(
                id = "content-reference",
                children=[
                    #html.H4("Reference:"),
                    dcc.Markdown('''
                            # Réference:  
                            [Kiva-site officiel](https://fr.wikipedia.org/wiki/Kiva_(organisation_philanthropique))  
                            [Kiva-Wikipedia](https://fr.wikipedia.org/wiki/Kiva_(organisation_philanthropique))  
                            [Kiva-api](https://www.kiva.org/build)

                    ''')  

                ]
        )   

    # elif value == 'tab-3':
    #     chld = html.Div(
    #             id = "content3",
    #             children=[
    #                 html.H4("Définition"),
    #                 html.B("page en construction")
    #             ]
    #     )

    elif value == 'tab-2':
        chld = html.Div(
            id = "content4",
            children=[
                html.H4(""),
                html.B("page en construction")
            ]
        )
        

    return chld 
        


# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)