
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
# import all pages in the app
from apps import prevision, home, reference

print('dash version: ', dcc.__version__) 

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py



nav_item = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/home", id="page-1-link")),
#        dbc.NavItem(dbc.NavLink("Analyse ML", href="/analyse", id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Prévision", href="/prevision", id="page-2-link")),    
        dbc.NavItem(dbc.NavLink("Référence", href="/reference", id="page-3-link")),
    ],
    fill= True,
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/simplon.png", height="30px"), className="ml-2"),
                ],
                className="page-1-link",
                align="center",
                no_gutters=True,
            ),
            href="/home",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Nav([nav_item], navbar=True, className="ml-2",)
    ],
    color="#4faf4e",
)


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)

def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/{i}" for i in ["home","prevision","reference"]]


# embedding the navigation bar
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar,

        dbc.Container(id="page-content", className="pt-1", fluid=True),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
              
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
        return home.layout
    # elif pathname == '/analyse':
    #     return analyse.layout
    elif pathname == '/prevision':
        return prevision.layout
    elif pathname == '/reference':
        return reference.layout
    else:  
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-primary"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(host='0.0.0.0', debug=True, port=8050)