import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Projet KIVA", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H3(children=' Prévoir la probabilité de financement par KIVA'
                                     )
                    , className="mb-4 text-center")
            ]),

        dbc.Row([
            dbc.Col(html.B(children='')
                    , className="mb-5 text-center")
        ]),

        dbc.Row([
            # dbc.Col(dbc.Card(children=[html.H3(children='Analyse ML',
            #                                    className="text-center"),
            #                             dbc.Button("ML",
            #                                       href="/analyse",
            #                                       color="success",
            #                                       className="mt-3"),
            #                            ],
            #                  body=True, color="dark", outline=True)
            #         , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Prévision',
                                               className="text-center"),
                                       dbc.Button("Prévision",
                                                  href="/prevision",
                                                  color="success",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    #, width=4, 
                    #className="mb-4"
            ),

            dbc.Col(dbc.Card(children=[html.H3(children='Référence',
                                               className="text-center"),
                                       dbc.Button("Référence",
                                                  href="/reference",
                                                  color="success",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                   # , width=4, 
                   # className="mb-4"
            ),
            # dbc.Col(dbc.Card(children=[html.H3(children='',
            #                                    className="text-center"),
            #                         #    dbc.Button("Référence",
            #                         #               href="/reference",
            #                         #               color="success",
            #                         #               className="mt-3"),
            #                            ],
            #                  body=True, color="dark", outline=True)
            #         , width=4, 
            #         className="mb-4"
            # )
        ], 
        #className="mb-4"
        ),

        dbc.Row([
            dbc.Col(html.A(children='')
                    , className="mb-5 text-center")
        ]),

        dbc.Row([
            dbc.Col(html.A(children='Simplon Microsoft - Developpeur Data IA')
                    , className="mb-5 text-center")
        ]),
 
        

    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)